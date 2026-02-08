#!/usr/bin/env python3
"""
通知模块
提供多种通知方式：邮件、短信、推送通知等
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import json
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
import asyncio
import aiohttp
from abc import ABC, abstractmethod
import time
from concurrent.futures import ThreadPoolExecutor
import queue
import threading
from enum import Enum

logger = logging.getLogger(__name__)


class NotificationType(Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    WEBHOOK = "webhook"
    SLACK = "slack"
    DISCORD = "discord"


class NotificationPriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class NotificationMessage:
    """通知消息"""
    type: NotificationType
    recipient: str
    subject: str
    body: str
    priority: NotificationPriority = NotificationPriority.NORMAL
    metadata: Dict[str, Any] = None
    template_id: Optional[str] = None
    attachments: List[Dict[str, Any]] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.attachments is None:
            self.attachments = []


@dataclass
class NotificationResult:
    """通知结果"""
    success: bool
    message_id: Optional[str] = None
    error_message: Optional[str] = None
    delivery_time: float = 0.0
    provider_response: Any = None


class NotificationProvider(ABC):
    """通知提供者抽象基类"""

    @abstractmethod
    async def send_notification(self, message: NotificationMessage) -> NotificationResult:
        """发送通知"""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """获取提供者名称"""
        pass


@dataclass
class EmailConfig:
    """邮件配置"""
    smtp_server: str
    smtp_port: int
    username: str
    password: str
    use_tls: bool = True
    from_email: str = None

    def __post_init__(self):
        if self.from_email is None:
            self.from_email = self.username


class EmailProvider(NotificationProvider):
    """邮件提供者"""

    def __init__(self, config: EmailConfig):
        self.config = config

    async def send_notification(self, message: NotificationMessage) -> NotificationResult:
        """发送邮件"""
        start_time = time.time()

        try:
            # 创建邮件
            email = MIMEMultipart()
            email["From"] = self.config.from_email
            email["To"] = message.recipient
            email["Subject"] = message.subject

            # 添加邮件正文
            body_part = MIMEText(message.body, "html" if "<" in message.body else "plain")
            email.attach(body_part)

            # 添加附件（简化实现）
            for attachment in message.attachments:
                # 这里可以实现附件添加逻辑
                pass

            # 发送邮件
            context = ssl.create_default_context() if self.config.use_tls else None

            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                if self.config.use_tls:
                    server.starttls(context=context)
                server.login(self.config.username, self.config.password)
                server.sendmail(self.config.from_email, message.recipient, email.as_string())

            delivery_time = time.time() - start_time
            message_id = f"email_{int(time.time())}_{hash(message.recipient)}"

            return NotificationResult(
                success=True,
                message_id=message_id,
                delivery_time=delivery_time
            )

        except Exception as e:
            delivery_time = time.time() - start_time
            logger.error(f"Email sending failed: {e}")
            return NotificationResult(
                success=False,
                error_message=str(e),
                delivery_time=delivery_time
            )

    def get_provider_name(self) -> str:
        return "EmailProvider"


@dataclass
class SMSConfig:
    """短信配置"""
    api_key: str
    api_secret: str
    provider_url: str
    sender_id: str = "System"


class SMSProvider(NotificationProvider):
    """短信提供者"""

    def __init__(self, config: SMSConfig):
        self.config = config

    async def send_notification(self, message: NotificationMessage) -> NotificationResult:
        """发送短信"""
        start_time = time.time()

        try:
            # 这里是模拟的短信发送逻辑
            # 实际实现需要根据具体 SMS 提供商的 API

            payload = {
                "to": message.recipient,
                "message": message.body,
                "sender": self.config.sender_id,
                "priority": message.priority.value
            }

            headers = {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(self.config.provider_url, json=payload, headers=headers) as response:
                    delivery_time = time.time() - start_time

                    if response.status == 200:
                        result_data = await response.json()
                        message_id = result_data.get("message_id", f"sms_{int(time.time())}")

                        return NotificationResult(
                            success=True,
                            message_id=message_id,
                            delivery_time=delivery_time,
                            provider_response=result_data
                        )
                    else:
                        error_text = await response.text()
                        return NotificationResult(
                            success=False,
                            error_message=f"SMS API error: {response.status} - {error_text}",
                            delivery_time=delivery_time
                        )

        except Exception as e:
            delivery_time = time.time() - start_time
            logger.error(f"SMS sending failed: {e}")
            return NotificationResult(
                success=False,
                error_message=str(e),
                delivery_time=delivery_time
            )

    def get_provider_name(self) -> str:
        return "SMSProvider"


@dataclass
class PushConfig:
    """推送通知配置"""
    server_key: str
    project_id: str
    api_url: str = "https://fcm.googleapis.com/fcm/send"


class PushProvider(NotificationProvider):
    """推送通知提供者"""

    def __init__(self, config: PushConfig):
        self.config = config

    async def send_notification(self, message: NotificationMessage) -> NotificationResult:
        """发送推送通知"""
        start_time = time.time()

        try:
            payload = {
                "to": message.recipient,  # FCM token
                "notification": {
                    "title": message.subject,
                    "body": message.body,
                    "icon": "default",
                    "click_action": "FLUTTER_NOTIFICATION_CLICK"
                },
                "data": message.metadata or {}
            }

            headers = {
                "Authorization": f"key={self.config.server_key}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(self.config.api_url, json=payload, headers=headers) as response:
                    delivery_time = time.time() - start_time

                    if response.status == 200:
                        result_data = await response.json()
                        message_id = result_data.get("multicast_id", f"push_{int(time.time())}")

                        return NotificationResult(
                            success=True,
                            message_id=str(message_id),
                            delivery_time=delivery_time,
                            provider_response=result_data
                        )
                    else:
                        error_text = await response.text()
                        return NotificationResult(
                            success=False,
                            error_message=f"Push API error: {response.status} - {error_text}",
                            delivery_time=delivery_time
                        )

        except Exception as e:
            delivery_time = time.time() - start_time
            logger.error(f"Push notification sending failed: {e}")
            return NotificationResult(
                success=False,
                error_message=str(e),
                delivery_time=delivery_time
            )

    def get_provider_name(self) -> str:
        return "PushProvider"


class NotificationTemplate:
    """通知模板"""

    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, Dict[str, str]]:
        """加载模板"""
        return {
            "welcome_email": {
                "subject": "Welcome to Our Platform, {{name}}!",
                "body": """
                <h1>Welcome {{name}}!</h1>
                <p>Thank you for joining our platform.</p>
                <p>Your account has been created successfully.</p>
                <p>Best regards,<br>The Team</p>
                """
            },
            "password_reset": {
                "subject": "Password Reset Request",
                "body": """
                <h2>Password Reset</h2>
                <p>Hello {{name}},</p>
                <p>You requested a password reset. Click the link below to reset your password:</p>
                <p><a href="{{reset_link}}">Reset Password</a></p>
                <p>This link will expire in 24 hours.</p>
                """
            },
            "user_activity": {
                "subject": "Account Activity Notification",
                "body": """
                <h2>Account Activity</h2>
                <p>Hello {{name}},</p>
                <p>We detected the following activity on your account:</p>
                <ul>
                <li>Action: {{action}}</li>
                <li>Time: {{timestamp}}</li>
                <li>IP Address: {{ip_address}}</li>
                </ul>
                <p>If this wasn't you, please contact support immediately.</p>
                """
            }
        }

    def render_template(self, template_id: str, variables: Dict[str, Any]) -> Optional[Dict[str, str]]:
        """渲染模板"""
        template = self.templates.get(template_id)
        if not template:
            return None

        rendered = {}
        for key, value in template.items():
            rendered[key] = self._replace_variables(value, variables)

        return rendered

    def _replace_variables(self, text: str, variables: Dict[str, Any]) -> str:
        """替换变量"""
        result = text
        for var, value in variables.items():
            result = result.replace("{{" + var + "}}", str(value))
        return result


class NotificationManager:
    """通知管理器"""

    def __init__(self):
        self.providers: Dict[NotificationType, NotificationProvider] = {}
        self.templates = NotificationTemplate()
        self.notification_queue = queue.Queue()
        self.executor = ThreadPoolExecutor(max_workers=20)
        self.is_running = False
        self.worker_thread = None

    def register_provider(self, notification_type: NotificationType, provider: NotificationProvider):
        """注册提供者"""
        self.providers[notification_type] = provider
        logger.info(f"Registered {provider.get_provider_name()} for {notification_type.value}")

    def unregister_provider(self, notification_type: NotificationType):
        """注销提供者"""
        if notification_type in self.providers:
            del self.providers[notification_type]
            logger.info(f"Unregistered provider for {notification_type.value}")

    def send_notification(self, message: NotificationMessage) -> NotificationResult:
        """发送通知"""
        provider = self.providers.get(message.type)
        if not provider:
            return NotificationResult(
                success=False,
                error_message=f"No provider registered for {message.type.value}"
            )

        # 如果是异步的，直接调用
        if asyncio.iscoroutinefunction(provider.send_notification):
            # 在线程池中运行异步函数
            future = self.executor.submit(asyncio.run, provider.send_notification(message))
            return future.result()
        else:
            # 同步调用
            return provider.send_notification(message)

    async def send_notification_async(self, message: NotificationMessage) -> NotificationResult:
        """异步发送通知"""
        provider = self.providers.get(message.type)
        if not provider:
            return NotificationResult(
                success=False,
                error_message=f"No provider registered for {message.type.value}"
            )

        return await provider.send_notification(message)

    def send_notification_from_template(self, template_id: str, variables: Dict[str, Any],
                                      notification_type: NotificationType, recipient: str) -> NotificationResult:
        """从模板发送通知"""
        template_data = self.templates.render_template(template_id, variables)
        if not template_data:
            return NotificationResult(
                success=False,
                error_message=f"Template {template_id} not found"
            )

        message = NotificationMessage(
            type=notification_type,
            recipient=recipient,
            subject=template_data["subject"],
            body=template_data["body"],
            template_id=template_id
        )

        return self.send_notification(message)

    def queue_notification(self, message: NotificationMessage):
        """将通知加入队列"""
        self.notification_queue.put(message)
        logger.info(f"Queued notification to {message.recipient}")

    def start_worker(self):
        """启动工作线程"""
        if self.is_running:
            return

        self.is_running = True
        self.worker_thread = threading.Thread(target=self._process_queue)
        self.worker_thread.daemon = True
        self.worker_thread.start()
        logger.info("Notification worker started")

    def stop_worker(self):
        """停止工作线程"""
        self.is_running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        logger.info("Notification worker stopped")

    def _process_queue(self):
        """处理通知队列"""
        while self.is_running:
            try:
                message = self.notification_queue.get(timeout=1)
                result = self.send_notification(message)

                if result.success:
                    logger.info(f"Successfully sent {message.type.value} to {message.recipient}")
                else:
                    logger.error(f"Failed to send {message.type.value} to {message.recipient}: {result.error_message}")

                self.notification_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error processing notification queue: {e}")

    def get_queue_size(self) -> int:
        """获取队列大小"""
        return self.notification_queue.qsize()

    def get_registered_providers(self) -> List[str]:
        """获取已注册的提供者"""
        return [f"{ntype.value}: {provider.get_provider_name()}"
                for ntype, provider in self.providers.items()]


# 全局通知管理器实例
_notification_manager = NotificationManager()


def get_notification_manager() -> NotificationManager:
    """获取通知管理器"""
    return _notification_manager


def initialize_notifications(email_config: EmailConfig = None,
                           sms_config: SMSConfig = None,
                           push_config: PushConfig = None):
    """初始化通知系统"""
    global _notification_manager

    if email_config:
        email_provider = EmailProvider(email_config)
        _notification_manager.register_provider(NotificationType.EMAIL, email_provider)

    if sms_config:
        sms_provider = SMSProvider(sms_config)
        _notification_manager.register_provider(NotificationType.SMS, sms_provider)

    if push_config:
        push_provider = PushProvider(push_config)
        _notification_manager.register_provider(NotificationType.PUSH, push_provider)

    # 启动工作线程
    _notification_manager.start_worker()

    logger.info("Notification system initialized")


def send_welcome_email(user_email: str, user_name: str) -> NotificationResult:
    """发送欢迎邮件"""
    return _notification_manager.send_notification_from_template(
        "welcome_email",
        {"name": user_name},
        NotificationType.EMAIL,
        user_email
    )


def send_password_reset_email(user_email: str, user_name: str, reset_link: str) -> NotificationResult:
    """发送密码重置邮件"""
    return _notification_manager.send_notification_from_template(
        "password_reset",
        {"name": user_name, "reset_link": reset_link},
        NotificationType.EMAIL,
        user_email
    )


def send_activity_notification(user_email: str, user_name: str, action: str, timestamp: str, ip_address: str) -> NotificationResult:
    """发送活动通知邮件"""
    return _notification_manager.send_notification_from_template(
        "user_activity",
        {
            "name": user_name,
            "action": action,
            "timestamp": timestamp,
            "ip_address": ip_address
        },
        NotificationType.EMAIL,
        user_email
    )


def queue_bulk_notifications(messages: List[NotificationMessage]):
    """批量队列通知"""
    for message in messages:
        _notification_manager.queue_notification(message)
    logger.info(f"Queued {len(messages)} bulk notifications")