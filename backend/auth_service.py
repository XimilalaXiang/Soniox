"""
认证服务模块
提供统一的认证逻辑封装，包括Cookie管理、密码验证等功能
"""
import hmac
import hashlib
import base64
import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Response


class AuthService:
    """认证服务类"""

    # 配置常量
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    COOKIE_NAME: str = "auth_token"
    TOKEN_TTL_SECONDS: int = 60 * 60 * 12  # 12小时

    @staticmethod
    def sign(payload: str) -> str:
        """
        生成签名的token

        Args:
            payload: 要签名的载荷

        Returns:
            签名后的token字符串
        """
        mac = hmac.new(
            AuthService.SECRET_KEY.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"{base64.urlsafe_b64encode(payload.encode()).decode()}.{mac}"

    @staticmethod
    def verify(token: str) -> bool:
        """
        验证token的有效性

        Args:
            token: 要验证的token

        Returns:
            token是否有效
        """
        try:
            data_b64, mac = token.split(".", 1)
            payload = base64.urlsafe_b64decode(data_b64.encode()).decode()

            # 验证签名
            if hmac.new(
                AuthService.SECRET_KEY.encode(),
                payload.encode(),
                hashlib.sha256
            ).hexdigest() != mac:
                return False

            # 解析过期时间
            parts = payload.split("|")
            exp = 0
            for p in parts:
                if p.startswith("exp:"):
                    exp = int(p.split(":", 1)[1])

            # 检查是否过期
            return int(datetime.utcnow().timestamp()) < exp

        except Exception:
            return False

    @staticmethod
    def set_auth_cookie(response: Response, ttl: int = None) -> None:
        """
        设置认证Cookie

        Args:
            response: FastAPI Response对象
            ttl: Cookie有效期（秒），默认12小时
        """
        if ttl is None:
            ttl = AuthService.TOKEN_TTL_SECONDS

        exp = int((datetime.utcnow() + timedelta(seconds=ttl)).timestamp())
        payload = f"auth|exp:{exp}"
        token = AuthService.sign(payload)

        response.set_cookie(
            AuthService.COOKIE_NAME,
            token,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=ttl,
            path="/",
        )

    @staticmethod
    def clear_auth_cookie(response: Response) -> None:
        """
        清除认证Cookie

        Args:
            response: FastAPI Response对象
        """
        response.delete_cookie(AuthService.COOKIE_NAME, path="/")

    @staticmethod
    def generate_salt() -> str:
        """
        生成随机盐值

        Returns:
            Base64编码的随机盐
        """
        return base64.urlsafe_b64encode(os.urandom(16)).decode()

    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        """
        哈希密码

        Args:
            password: 原始密码
            salt: 盐值

        Returns:
            格式化的哈希密码：v1${salt}${digest}
        """
        digest = hashlib.sha256((salt + password).encode()).hexdigest()
        return f"v1${salt}${digest}"

    @staticmethod
    def verify_password(stored: str, password: str) -> bool:
        """
        验证密码是否匹配

        Args:
            stored: 存储的哈希密码
            password: 要验证的密码

        Returns:
            密码是否匹配
        """
        try:
            ver, salt, digest = stored.split("$", 2)
            if ver != "v1":
                return False
            return hashlib.sha256((salt + password).encode()).hexdigest() == digest
        except Exception:
            return False

