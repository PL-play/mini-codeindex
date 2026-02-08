#!/usr/bin/env python3
"""
API 客户端模块
提供外部 API 集成功能
"""

import requests
import aiohttp
import asyncio
from typing import Dict, Any, List, Optional, Union
import json
import logging
from dataclasses import dataclass
import time
from functools import wraps
import jwt
import hashlib
import hmac
import base64
from urllib.parse import urlencode
import threading
from concurrent.futures import ThreadPoolExecutor
import backoff

logger = logging.getLogger(__name__)


@dataclass
class APIConfig:
    """API 配置"""
    base_url: str
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    timeout: int = 30
    retries: int = 3
    rate_limit: int = 100  # requests per minute
    auth_type: str = "bearer"  # bearer, basic, api_key, hmac


@dataclass
class APIResponse:
    """API 响应"""
    status_code: int
    data: Any
    headers: Dict[str, str]
    success: bool
    error_message: Optional[str] = None
    request_time: float = 0.0


class APIError(Exception):
    """API 异常"""
    def __init__(self, message: str, status_code: int = 0, response_data: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class RateLimiter:
    """速率限制器"""

    def __init__(self, requests_per_minute: int):
        self.requests_per_minute = requests_per_minute
        self.requests = []
        self.lock = threading.Lock()

    def wait_if_needed(self):
        """如果需要，等待以遵守速率限制"""
        with self.lock:
            now = time.time()
            # 移除一分钟前的请求
            self.requests = [req_time for req_time in self.requests if now - req_time < 60]

            if len(self.requests) >= self.requests_per_minute:
                # 计算需要等待的时间
                oldest_request = min(self.requests)
                wait_time = 60 - (now - oldest_request)
                if wait_time > 0:
                    time.sleep(wait_time)

            self.requests.append(now)


class APIClient:
    """API 客户端基类"""

    def __init__(self, config: APIConfig):
        self.config = config
        self.session = requests.Session()
        self.rate_limiter = RateLimiter(config.rate_limit)
        self._setup_auth()

    def _setup_auth(self):
        """设置认证"""
        if self.config.auth_type == "bearer" and self.config.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.config.api_key}"})
        elif self.config.auth_type == "basic" and self.config.api_key and self.config.api_secret:
            auth = requests.auth.HTTPBasicAuth(self.config.api_key, self.config.api_secret)
            self.session.auth = auth
        elif self.config.auth_type == "api_key" and self.config.api_key:
            self.session.headers.update({"X-API-Key": self.config.api_key})

    def _generate_hmac_signature(self, method: str, path: str, body: str = "", timestamp: str = None) -> str:
        """生成 HMAC 签名"""
        if not self.config.api_secret:
            return ""

        if timestamp is None:
            timestamp = str(int(time.time()))

        message = f"{method}{path}{body}{timestamp}"
        signature = hmac.new(
            self.config.api_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()

        return base64.b64encode(signature).decode()

    @backoff.on_exception(backoff.expo, (requests.RequestException, APIError), max_tries=3)
    def _make_request(self, method: str, endpoint: str, **kwargs) -> APIResponse:
        """发起请求"""
        self.rate_limiter.wait_if_needed()

        url = f"{self.config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        # 添加 HMAC 认证
        if self.config.auth_type == "hmac":
            timestamp = str(int(time.time()))
            body = kwargs.get('data', '') or kwargs.get('json', '') or ''
            if isinstance(body, dict):
                body = json.dumps(body, sort_keys=True)

            signature = self._generate_hmac_signature(method.upper(), endpoint, body, timestamp)
            self.session.headers.update({
                "X-Timestamp": timestamp,
                "X-Signature": signature
            })

        start_time = time.time()
        try:
            response = self.session.request(method, url, timeout=self.config.timeout, **kwargs)
            request_time = time.time() - start_time

            if response.status_code >= 400:
                error_data = None
                try:
                    error_data = response.json()
                except:
                    error_data = response.text

                raise APIError(
                    f"API request failed: {response.status_code}",
                    response.status_code,
                    error_data
                )

            # 尝试解析 JSON
            try:
                data = response.json()
            except:
                data = response.text

            return APIResponse(
                status_code=response.status_code,
                data=data,
                headers=dict(response.headers),
                success=True,
                request_time=request_time
            )

        except requests.RequestException as e:
            request_time = time.time() - start_time
            return APIResponse(
                status_code=0,
                data=None,
                headers={},
                success=False,
                error_message=str(e),
                request_time=request_time
            )

    def get(self, endpoint: str, params: Dict[str, Any] = None, **kwargs) -> APIResponse:
        """GET 请求"""
        return self._make_request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: Any = None, json_data: Dict[str, Any] = None, **kwargs) -> APIResponse:
        """POST 请求"""
        if json_data:
            kwargs['json'] = json_data
        elif data:
            kwargs['data'] = data
        return self._make_request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, data: Any = None, json_data: Dict[str, Any] = None, **kwargs) -> APIResponse:
        """PUT 请求"""
        if json_data:
            kwargs['json'] = json_data
        elif data:
            kwargs['data'] = data
        return self._make_request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> APIResponse:
        """DELETE 请求"""
        return self._make_request("DELETE", endpoint, **kwargs)


class AsyncAPIClient:
    """异步 API 客户端"""

    def __init__(self, config: APIConfig):
        self.config = config
        self.rate_limiter = RateLimiter(config.rate_limit)
        self._auth_headers = self._setup_auth()

    def _setup_auth(self) -> Dict[str, str]:
        """设置认证头"""
        headers = {}
        if self.config.auth_type == "bearer" and self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        elif self.config.auth_type == "api_key" and self.config.api_key:
            headers["X-API-Key"] = self.config.api_key
        return headers

    async def _make_request(self, method: str, endpoint: str, **kwargs) -> APIResponse:
        """发起异步请求"""
        self.rate_limiter.wait_if_needed()

        url = f"{self.config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        headers = {**self._auth_headers}
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])

        start_time = time.time()

        async with aiohttp.ClientSession(headers=headers, timeout=aiohttp.ClientTimeout(total=self.config.timeout)) as session:
            try:
                async with session.request(method, url, **kwargs) as response:
                    request_time = time.time() - start_time

                    if response.status >= 400:
                        error_data = None
                        try:
                            error_data = await response.json()
                        except:
                            error_data = await response.text()

                        raise APIError(
                            f"Async API request failed: {response.status}",
                            response.status,
                            error_data
                        )

                    # 尝试解析 JSON
                    try:
                        data = await response.json()
                    except:
                        data = await response.text()

                    return APIResponse(
                        status_code=response.status,
                        data=data,
                        headers=dict(response.headers),
                        success=True,
                        request_time=request_time
                    )

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                request_time = time.time() - start_time
                return APIResponse(
                    status_code=0,
                    data=None,
                    headers={},
                    success=False,
                    error_message=str(e),
                    request_time=request_time
                )

    async def get(self, endpoint: str, params: Dict[str, Any] = None, **kwargs) -> APIResponse:
        """异步 GET 请求"""
        if params:
            kwargs['params'] = params
        return await self._make_request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, data: Any = None, json_data: Dict[str, Any] = None, **kwargs) -> APIResponse:
        """异步 POST 请求"""
        if json_data:
            kwargs['json'] = json_data
        elif data:
            kwargs['data'] = data
        return await self._make_request("POST", endpoint, **kwargs)


class UserAPIClient(APIClient):
    """用户 API 客户端"""

    def __init__(self, config: APIConfig):
        super().__init__(config)

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """获取用户"""
        response = self.get(f"/users/{user_id}")
        return response.data if response.success else None

    def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """创建用户"""
        response = self.post("/users", json_data=user_data)
        return response.data if response.success else None

    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> bool:
        """更新用户"""
        response = self.put(f"/users/{user_id}", json_data=user_data)
        return response.success

    def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        response = self.delete(f"/users/{user_id}")
        return response.success

    def search_users(self, query: str, department: str = None) -> List[Dict[str, Any]]:
        """搜索用户"""
        params = {"q": query}
        if department:
            params["department"] = department

        response = self.get("/users/search", params=params)
        return response.data if response.success else []

    def get_department_users(self, department: str) -> List[Dict[str, Any]]:
        """获取部门用户"""
        response = self.get(f"/departments/{department}/users")
        return response.data if response.success else []


class NotificationAPIClient(APIClient):
    """通知 API 客户端"""

    def __init__(self, config: APIConfig):
        super().__init__(config)

    def send_email(self, to: str, subject: str, body: str, template_id: str = None) -> bool:
        """发送邮件"""
        data = {
            "to": to,
            "subject": subject,
            "body": body
        }
        if template_id:
            data["template_id"] = template_id

        response = self.post("/notifications/email", json_data=data)
        return response.success

    def send_sms(self, to: str, message: str) -> bool:
        """发送短信"""
        data = {
            "to": to,
            "message": message
        }
        response = self.post("/notifications/sms", json_data=data)
        return response.success

    def send_push_notification(self, user_id: str, title: str, message: str, data: Dict[str, Any] = None) -> bool:
        """发送推送通知"""
        payload = {
            "user_id": user_id,
            "title": title,
            "message": message,
            "data": data or {}
        }
        response = self.post("/notifications/push", json_data=payload)
        return response.success

    def get_notification_history(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """获取通知历史"""
        response = self.get(f"/notifications/history/{user_id}", params={"limit": limit})
        return response.data if response.success else []


class AnalyticsAPIClient(APIClient):
    """分析 API 客户端"""

    def __init__(self, config: APIConfig):
        super().__init__(config)

    def track_event(self, event_name: str, user_id: str, properties: Dict[str, Any] = None) -> bool:
        """跟踪事件"""
        data = {
            "event_name": event_name,
            "user_id": user_id,
            "properties": properties or {},
            "timestamp": int(time.time())
        }
        response = self.post("/analytics/events", json_data=data)
        return response.success

    def get_user_analytics(self, user_id: str, start_date: str, end_date: str) -> Optional[Dict[str, Any]]:
        """获取用户分析数据"""
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        response = self.get(f"/analytics/users/{user_id}", params=params)
        return response.data if response.success else None

    def get_system_metrics(self) -> Optional[Dict[str, Any]]:
        """获取系统指标"""
        response = self.get("/analytics/system/metrics")
        return response.data if response.success else None


class ExternalServiceIntegrator:
    """外部服务集成器"""

    def __init__(self):
        self.user_api = None
        self.notification_api = None
        self.analytics_api = None
        self.executor = ThreadPoolExecutor(max_workers=10)

    def configure_user_api(self, config: APIConfig):
        """配置用户 API"""
        self.user_api = UserAPIClient(config)

    def configure_notification_api(self, config: APIConfig):
        """配置通知 API"""
        self.notification_api = NotificationAPIClient(config)

    def configure_analytics_api(self, config: APIConfig):
        """配置分析 API"""
        self.analytics_api = AnalyticsAPIClient(config)

    def sync_user_from_external(self, external_user_id: str) -> Optional[Dict[str, Any]]:
        """从外部服务同步用户"""
        if not self.user_api:
            return None

        # 这里可以实现复杂的同步逻辑
        external_user = self.user_api.get_user(external_user_id)
        if external_user:
            # 转换数据格式
            internal_user = self._transform_external_user(external_user)
            # 保存到本地数据库
            # 这里可以调用 database 模块
            return internal_user
        return None

    def _transform_external_user(self, external_user: Dict[str, Any]) -> Dict[str, Any]:
        """转换外部用户数据"""
        return {
            "id": external_user.get("external_id"),
            "name": external_user.get("full_name"),
            "email": external_user.get("email_address"),
            "age": external_user.get("age_years"),
            "department": external_user.get("organization"),
            "skills": external_user.get("competencies", []),
            "metadata": {
                "external_id": external_user.get("id"),
                "source": "external_api",
                "last_sync": int(time.time())
            }
        }

    def notify_user_action(self, user_id: str, action: str, details: Dict[str, Any]):
        """通知用户操作"""
        if not self.notification_api:
            return

        # 并行发送多种通知
        futures = []

        # 邮件通知
        email_future = self.executor.submit(
            self.notification_api.send_email,
            f"user_{user_id}@company.com",
            f"Action Performed: {action}",
            f"You performed action: {action}\nDetails: {json.dumps(details, indent=2)}"
        )
        futures.append(email_future)

        # 推送通知
        push_future = self.executor.submit(
            self.notification_api.send_push_notification,
            user_id,
            "Action Completed",
            f"Your {action} has been completed successfully",
            details
        )
        futures.append(push_future)

        # 等待所有通知完成
        for future in futures:
            try:
                future.result(timeout=10)
            except Exception as e:
                logger.error(f"Notification failed: {e}")

    def track_user_activity(self, user_id: str, activity: str, metadata: Dict[str, Any]):
        """跟踪用户活动"""
        if not self.analytics_api:
            return

        self.analytics_api.track_event(
            f"user_{activity}",
            user_id,
            {
                "activity": activity,
                "metadata": metadata,
                "timestamp": int(time.time())
            }
        )


# 全局集成器实例
_integrator = ExternalServiceIntegrator()


def get_external_integrator() -> ExternalServiceIntegrator:
    """获取外部服务集成器"""
    return _integrator


def initialize_external_services(user_api_config: APIConfig = None,
                               notification_config: APIConfig = None,
                               analytics_config: APIConfig = None):
    """初始化外部服务"""
    global _integrator

    if user_api_config:
        _integrator.configure_user_api(user_api_config)

    if notification_config:
        _integrator.configure_notification_api(notification_config)

    if analytics_config:
        _integrator.configure_analytics_api(analytics_config)

    logger.info("External services initialized")