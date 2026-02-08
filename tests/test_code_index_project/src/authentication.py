"""
Authentication module for user management system.
Handles user authentication, session management, and security features.
"""

import asyncio
import hashlib
import hmac
import json
import logging
import secrets
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any, Callable
from concurrent.futures import ThreadPoolExecutor
import threading
import jwt
import bcrypt
from functools import wraps, lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Base exception for authentication errors."""
    pass


class InvalidCredentialsError(AuthenticationError):
    """Raised when invalid credentials are provided."""
    pass


class AccountLockedError(AuthenticationError):
    """Raised when account is locked due to security reasons."""
    pass


class SessionExpiredError(AuthenticationError):
    """Raised when session has expired."""
    pass


class TokenValidationError(AuthenticationError):
    """Raised when token validation fails."""
    pass


class UserStatus(Enum):
    """User account status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOCKED = "locked"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"


class AuthenticationMethod(Enum):
    """Supported authentication methods."""
    PASSWORD = "password"
    TWO_FACTOR = "two_factor"
    BIOMETRIC = "biometric"
    SSO = "sso"
    API_KEY = "api_key"


@dataclass
class User:
    """User data class with authentication information."""
    user_id: str
    username: str
    email: str
    password_hash: str
    status: UserStatus = UserStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    login_attempts: int = 0
    lockout_until: Optional[datetime] = None
    two_factor_enabled: bool = False
    two_factor_secret: Optional[str] = None
    password_reset_token: Optional[str] = None
    password_reset_expires: Optional[datetime] = None
    roles: Set[str] = field(default_factory=set)
    permissions: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_locked(self) -> bool:
        """Check if user account is currently locked."""
        if self.status == UserStatus.LOCKED:
            return True
        if self.lockout_until and datetime.now() < self.lockout_until:
            return True
        return False

    def can_login(self) -> bool:
        """Check if user can attempt to login."""
        return (self.status == UserStatus.ACTIVE and
                not self.is_locked() and
                self.login_attempts < 5)

    def record_login_attempt(self, success: bool):
        """Record a login attempt."""
        if success:
            self.login_attempts = 0
            self.last_login = datetime.now()
            self.lockout_until = None
        else:
            self.login_attempts += 1
            if self.login_attempts >= 5:
                self.lockout_until = datetime.now() + timedelta(minutes=30)

    def reset_password(self, new_password: str):
        """Reset user password."""
        self.password_hash = self._hash_password(new_password)
        self.password_reset_token = None
        self.password_reset_expires = None
        self.updated_at = datetime.now()

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))


@dataclass
class Session:
    """User session data class."""
    session_id: str
    user_id: str
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=8))
    last_activity: datetime = field(default_factory=datetime.now)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    is_active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        """Check if session has expired."""
        return datetime.now() > self.expires_at

    def extend(self, duration_hours: int = 8):
        """Extend session expiration."""
        self.expires_at = datetime.now() + timedelta(hours=duration_hours)
        self.last_activity = datetime.now()

    def invalidate(self):
        """Invalidate the session."""
        self.is_active = False


@dataclass
class AuthToken:
    """Authentication token data class."""
    token: str
    token_type: str = "Bearer"
    user_id: str = ""
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=1))
    scopes: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        """Check if token has expired."""
        return datetime.now() > self.expires_at


class AuthConfig:
    """Authentication configuration class."""
    def __init__(self):
        self.jwt_secret = secrets.token_hex(32)
        self.jwt_algorithm = "HS256"
        self.session_timeout_hours = 8
        self.token_timeout_hours = 1
        self.max_login_attempts = 5
        self.lockout_duration_minutes = 30
        self.password_min_length = 8
        self.enable_two_factor = False
        self.enable_session_management = True
        self.enable_audit_logging = True
        self.allowed_origins: Set[str] = set()
        self.rate_limit_attempts = 10
        self.rate_limit_window_minutes = 15


class AuthenticationService:
    """Main authentication service class."""

    def __init__(self, config: AuthConfig = None, user_store: 'UserStore' = None):
        self.config = config or AuthConfig()
        self.user_store = user_store or InMemoryUserStore()
        self.session_store = InMemorySessionStore()
        self.token_store = InMemoryTokenStore()
        self.audit_logger = AuditLogger()
        self.rate_limiter = RateLimiter(self.config.rate_limit_attempts,
                                      self.config.rate_limit_window_minutes)
        self._executor = ThreadPoolExecutor(max_workers=4)
        self._lock = threading.RLock()

    async def authenticate_user(self, username: str, password: str,
                              ip_address: str = None, user_agent: str = None) -> Tuple[User, Session]:
        """Authenticate user with username and password."""
        # Rate limiting check
        if not self.rate_limiter.check_limit(f"login:{username}"):
            raise AuthenticationError("Too many login attempts. Please try again later.")

        try:
            # Get user
            user = await self.user_store.get_user_by_username(username)
            if not user:
                raise InvalidCredentialsError("Invalid username or password")

            # Check account status
            if not user.can_login():
                if user.is_locked():
                    raise AccountLockedError("Account is locked due to security reasons")
                raise AuthenticationError("Account is not active")

            # Verify password
            if not user.verify_password(password):
                user.record_login_attempt(False)
                await self.user_store.update_user(user)
                await self.audit_logger.log_failed_login(username, ip_address, "invalid_password")
                raise InvalidCredentialsError("Invalid username or password")

            # Successful authentication
            user.record_login_attempt(True)
            await self.user_store.update_user(user)

            # Create session
            session = await self._create_session(user, ip_address, user_agent)

            # Log successful login
            await self.audit_logger.log_successful_login(user.user_id, ip_address, user_agent)

            return user, session

        except AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"Authentication error for user {username}: {e}")
            raise AuthenticationError("Authentication failed")

    async def authenticate_token(self, token: str) -> Tuple[User, Session]:
        """Authenticate user using JWT token."""
        try:
            # Decode and validate token
            payload = jwt.decode(token, self.config.jwt_secret,
                               algorithms=[self.config.jwt_algorithm])

            user_id = payload.get('user_id')
            session_id = payload.get('session_id')

            if not user_id or not session_id:
                raise TokenValidationError("Invalid token payload")

            # Get user and session
            user = await self.user_store.get_user(user_id)
            session = await self.session_store.get_session(session_id)

            if not user or not session:
                raise TokenValidationError("Invalid token")

            if not session.is_active or session.is_expired():
                raise SessionExpiredError("Session expired")

            # Extend session
            session.extend()
            await self.session_store.update_session(session)

            return user, session

        except jwt.ExpiredSignatureError:
            raise TokenValidationError("Token expired")
        except jwt.InvalidTokenError:
            raise TokenValidationError("Invalid token")

    async def create_token(self, user: User, session: Session, scopes: Set[str] = None) -> AuthToken:
        """Create JWT token for authenticated user."""
        expires_at = datetime.now() + timedelta(hours=self.config.token_timeout_hours)

        payload = {
            'user_id': user.user_id,
            'session_id': session.session_id,
            'scopes': list(scopes or set()),
            'iat': int(time.time()),
            'exp': int(expires_at.timestamp())
        }

        token = jwt.encode(payload, self.config.jwt_secret,
                          algorithm=self.config.jwt_algorithm)

        auth_token = AuthToken(
            token=token,
            user_id=user.user_id,
            expires_at=expires_at,
            scopes=scopes or set()
        )

        await self.token_store.store_token(auth_token)
        return auth_token

    async def logout_user(self, session_id: str):
        """Logout user by invalidating session."""
        session = await self.session_store.get_session(session_id)
        if session:
            session.invalidate()
            await self.session_store.update_session(session)
            await self.audit_logger.log_logout(session.user_id)

    async def initiate_password_reset(self, email: str) -> str:
        """Initiate password reset process."""
        user = await self.user_store.get_user_by_email(email)
        if not user:
            # Don't reveal if email exists
            return "If the email exists, a reset link has been sent."

        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=24)

        user.password_reset_token = reset_token
        user.password_reset_expires = expires_at
        await self.user_store.update_user(user)

        # In real implementation, send email here
        await self.audit_logger.log_password_reset_initiated(user.user_id, email)

        return "If the email exists, a reset link has been sent."

    async def reset_password(self, reset_token: str, new_password: str):
        """Reset password using reset token."""
        if len(new_password) < self.config.password_min_length:
            raise AuthenticationError(f"Password must be at least {self.config.password_min_length} characters")

        user = await self.user_store.get_user_by_reset_token(reset_token)
        if not user or not user.password_reset_expires or datetime.now() > user.password_reset_expires:
            raise AuthenticationError("Invalid or expired reset token")

        user.reset_password(new_password)
        await self.user_store.update_user(user)
        await self.audit_logger.log_password_reset_completed(user.user_id)

    async def change_password(self, user_id: str, old_password: str, new_password: str):
        """Change user password."""
        user = await self.user_store.get_user(user_id)
        if not user:
            raise AuthenticationError("User not found")

        if not user.verify_password(old_password):
            raise AuthenticationError("Current password is incorrect")

        if len(new_password) < self.config.password_min_length:
            raise AuthenticationError(f"Password must be at least {self.config.password_min_length} characters")

        user.reset_password(new_password)
        await self.user_store.update_user(user)
        await self.audit_logger.log_password_changed(user_id)

    async def enable_two_factor(self, user_id: str, secret: str):
        """Enable two-factor authentication for user."""
        user = await self.user_store.get_user(user_id)
        if not user:
            raise AuthenticationError("User not found")

        user.two_factor_enabled = True
        user.two_factor_secret = secret
        await self.user_store.update_user(user)
        await self.audit_logger.log_two_factor_enabled(user_id)

    async def verify_two_factor(self, user_id: str, code: str) -> bool:
        """Verify two-factor authentication code."""
        user = await self.user_store.get_user(user_id)
        if not user or not user.two_factor_enabled or not user.two_factor_secret:
            return False

        # In real implementation, verify TOTP code
        # For demo purposes, accept any 6-digit code
        return len(code) == 6 and code.isdigit()

    def require_auth(self, scopes: Set[str] = None):
        """Decorator to require authentication for endpoints."""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Extract token from request (simplified)
                token = kwargs.get('token') or getattr(args[0] if args else None, 'token', None)
                if not token:
                    raise AuthenticationError("Authentication required")

                user, session = await self.authenticate_token(token)

                # Check scopes
                if scopes:
                    token_obj = await self.token_store.get_token(token)
                    if not token_obj or not scopes.issubset(token_obj.scopes):
                        raise AuthenticationError("Insufficient permissions")

                kwargs['user'] = user
                kwargs['session'] = session
                return await func(*args, **kwargs)
            return wrapper
        return decorator

    async def cleanup_expired_sessions(self):
        """Clean up expired sessions."""
        await self.session_store.cleanup_expired()

    async def get_user_sessions(self, user_id: str) -> List[Session]:
        """Get all active sessions for a user."""
        return await self.session_store.get_user_sessions(user_id)

    async def invalidate_user_sessions(self, user_id: str, except_session_id: str = None):
        """Invalidate all sessions for a user except optionally one."""
        sessions = await self.get_user_sessions(user_id)
        for session in sessions:
            if except_session_id is None or session.session_id != except_session_id:
                session.invalidate()
                await self.session_store.update_session(session)

    async def _create_session(self, user: User, ip_address: str = None,
                            user_agent: str = None) -> Session:
        """Create a new session for user."""
        session = Session(
            session_id=secrets.token_hex(32),
            user_id=user.user_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        await self.session_store.store_session(session)
        return session


class RateLimiter:
    """Rate limiter for authentication attempts."""

    def __init__(self, max_attempts: int, window_minutes: int):
        self.max_attempts = max_attempts
        self.window_seconds = window_minutes * 60
        self.attempts: Dict[str, List[float]] = {}
        self._lock = threading.Lock()

    def check_limit(self, key: str) -> bool:
        """Check if request is within rate limit."""
        with self._lock:
            now = time.time()
            if key not in self.attempts:
                self.attempts[key] = []

            # Remove old attempts outside window
            self.attempts[key] = [t for t in self.attempts[key]
                                if now - t < self.window_seconds]

            if len(self.attempts[key]) >= self.max_attempts:
                return False

            self.attempts[key].append(now)
            return True


class AuditLogger:
    """Audit logger for authentication events."""

    async def log_successful_login(self, user_id: str, ip_address: str = None,
                                 user_agent: str = None):
        """Log successful login."""
        logger.info(f"Successful login: user={user_id}, ip={ip_address}")

    async def log_failed_login(self, username: str, ip_address: str = None,
                             reason: str = None):
        """Log failed login attempt."""
        logger.warning(f"Failed login attempt: username={username}, ip={ip_address}, reason={reason}")

    async def log_logout(self, user_id: str):
        """Log user logout."""
        logger.info(f"User logout: user={user_id}")

    async def log_password_reset_initiated(self, user_id: str, email: str):
        """Log password reset initiation."""
        logger.info(f"Password reset initiated: user={user_id}, email={email}")

    async def log_password_reset_completed(self, user_id: str):
        """Log password reset completion."""
        logger.info(f"Password reset completed: user={user_id}")

    async def log_password_changed(self, user_id: str):
        """Log password change."""
        logger.info(f"Password changed: user={user_id}")

    async def log_two_factor_enabled(self, user_id: str):
        """Log two-factor authentication enabled."""
        logger.info(f"Two-factor authentication enabled: user={user_id}")


# Storage interfaces and implementations
class UserStore:
    """Abstract base class for user storage."""
    async def get_user(self, user_id: str) -> Optional[User]:
        raise NotImplementedError

    async def get_user_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError

    async def get_user_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    async def get_user_by_reset_token(self, reset_token: str) -> Optional[User]:
        raise NotImplementedError

    async def update_user(self, user: User):
        raise NotImplementedError

    async def create_user(self, user: User):
        raise NotImplementedError


class InMemoryUserStore(UserStore):
    """In-memory user store implementation."""

    def __init__(self):
        self.users: Dict[str, User] = {}
        self.username_index: Dict[str, str] = {}
        self.email_index: Dict[str, str] = {}
        self.reset_token_index: Dict[str, str] = {}

    async def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        user_id = self.username_index.get(username)
        return self.users.get(user_id) if user_id else None

    async def get_user_by_email(self, email: str) -> Optional[User]:
        user_id = self.email_index.get(email)
        return self.users.get(user_id) if user_id else None

    async def get_user_by_reset_token(self, reset_token: str) -> Optional[User]:
        user_id = self.reset_token_index.get(reset_token)
        return self.users.get(user_id) if user_id else None

    async def update_user(self, user: User):
        self.users[user.user_id] = user
        self.username_index[user.username] = user.user_id
        self.email_index[user.email] = user.user_id
        if user.password_reset_token:
            self.reset_token_index[user.password_reset_token] = user.user_id

    async def create_user(self, user: User):
        await self.update_user(user)


class SessionStore:
    """Abstract base class for session storage."""
    async def store_session(self, session: Session):
        raise NotImplementedError

    async def get_session(self, session_id: str) -> Optional[Session]:
        raise NotImplementedError

    async def update_session(self, session: Session):
        raise NotImplementedError

    async def get_user_sessions(self, user_id: str) -> List[Session]:
        raise NotImplementedError

    async def cleanup_expired(self):
        raise NotImplementedError


class InMemorySessionStore(SessionStore):
    """In-memory session store implementation."""

    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self.user_sessions: Dict[str, Set[str]] = {}

    async def store_session(self, session: Session):
        self.sessions[session.session_id] = session
        self.user_sessions.computeIfAbsent(session.user_id, lambda: set()).add(session.session_id)

    async def get_session(self, session_id: str) -> Optional[Session]:
        return self.sessions.get(session_id)

    async def update_session(self, session: Session):
        self.sessions[session.session_id] = session

    async def get_user_sessions(self, user_id: str) -> List[Session]:
        session_ids = self.user_sessions.get(user_id, set())
        return [self.sessions[sid] for sid in session_ids if sid in self.sessions]

    async def cleanup_expired(self):
        expired_sessions = [sid for sid, session in self.sessions.items()
                          if session.is_expired() or not session.is_active]
        for sid in expired_sessions:
            session = self.sessions[sid]
            self.sessions.pop(sid, None)
            self.user_sessions.get(session.user_id, set()).discard(sid)


class TokenStore:
    """Abstract base class for token storage."""
    async def store_token(self, token: AuthToken):
        raise NotImplementedError

    async def get_token(self, token_str: str) -> Optional[AuthToken]:
        raise NotImplementedError

    async def invalidate_token(self, token_str: str):
        raise NotImplementedError


class InMemoryTokenStore(TokenStore):
    """In-memory token store implementation."""

    def __init__(self):
        self.tokens: Dict[str, AuthToken] = {}

    async def store_token(self, token: AuthToken):
        self.tokens[token.token] = token

    async def get_token(self, token_str: str) -> Optional[AuthToken]:
        return self.tokens.get(token_str)

    async def invalidate_token(self, token_str: str):
        self.tokens.pop(token_str, None)


# Utility functions
def generate_password_hash(password: str) -> str:
    """Generate password hash."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def generate_secure_token(length: int = 32) -> str:
    """Generate secure random token."""
    return secrets.token_urlsafe(length)


def hash_string(data: str, salt: str = None) -> str:
    """Hash string with optional salt."""
    if salt:
        data = data + salt
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def create_hmac_signature(data: str, key: str) -> str:
    """Create HMAC signature."""
    return hmac.new(key.encode('utf-8'), data.encode('utf-8'),
                   hashlib.sha256).hexdigest()


# Example usage and test functions
async def example_usage():
    """Example usage of the authentication service."""
    # Create service
    auth_service = AuthenticationService()

    # Create a test user
    test_user = User(
        user_id="user123",
        username="testuser",
        email="test@example.com",
        password_hash=generate_password_hash("password123"),
        roles={"user"},
        permissions={"read", "write"}
    )
    await auth_service.user_store.create_user(test_user)

    try:
        # Authenticate user
        user, session = await auth_service.authenticate_user("testuser", "password123")
        print(f"Authenticated user: {user.username}")

        # Create token
        token = await auth_service.create_token(user, session, {"read", "write"})
        print(f"Created token: {token.token[:20]}...")

        # Verify token
        verified_user, verified_session = await auth_service.authenticate_token(token.token)
        print(f"Verified user: {verified_user.username}")

    except AuthenticationError as e:
        print(f"Authentication error: {e}")


if __name__ == "__main__":
    asyncio.run(example_usage())