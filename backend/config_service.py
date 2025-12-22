"""
配置服务模块
提供统一的配置管理逻辑，包括设置存取、配置加载等功能
"""
import json
from typing import Optional
from database import SettingDB, async_session_maker
from models import OpenAIConfig


class ConfigService:
    """配置服务类"""

    # 配置键常量
    KEY_PASSWORD_HASH = "password_hash"
    KEY_SONIOX_CONFIG = "soniox_config"
    KEY_OPENAI_CONFIG = "openai_config"
    KEY_SONIOX_API_KEY = "soniox_api_key"
    KEY_OPENAI_API_KEY = "openai_api_key"

    @staticmethod
    async def get_setting(key: str) -> Optional[str]:
        """
        获取配置值

        Args:
            key: 配置键

        Returns:
            配置值，不存在则返回None
        """
        async with async_session_maker() as session:
            row = await session.get(SettingDB, key)
            return row.value if row else None

    @staticmethod
    async def set_setting(key: str, value: str) -> None:
        """
        设置配置值

        Args:
            key: 配置键
            value: 配置值
        """
        async with async_session_maker() as session:
            row = await session.get(SettingDB, key)
            if row:
                row.value = value
            else:
                row = SettingDB(key=key, value=value)
                session.add(row)
            await session.commit()

    @staticmethod
    async def get_soniox_config() -> dict:
        """
        获取Soniox配置

        Returns:
            Soniox配置字典
        """
        config_raw = await ConfigService.get_setting(ConfigService.KEY_SONIOX_CONFIG) or "{}"
        try:
            return json.loads(config_raw) if config_raw else {}
        except Exception:
            return {}

    @staticmethod
    async def set_soniox_config(config: dict, api_key: str = None) -> None:
        """
        保存Soniox配置

        Args:
            config: Soniox配置字典
            api_key: API密钥（可选，单独存储）
        """
        if api_key:
            await ConfigService.set_setting(ConfigService.KEY_SONIOX_API_KEY, api_key)

        config_slim = {k: v for k, v in config.items() if k != "api_key"}
        await ConfigService.set_setting(
            ConfigService.KEY_SONIOX_CONFIG,
            json.dumps(config_slim)
        )

    @staticmethod
    async def get_openai_config() -> dict:
        """
        获取OpenAI配置

        Returns:
            OpenAI配置字典
        """
        config_raw = await ConfigService.get_setting(ConfigService.KEY_OPENAI_CONFIG) or "{}"
        try:
            return json.loads(config_raw) if config_raw else {}
        except Exception:
            return {}

    @staticmethod
    async def set_openai_config(config: dict, api_key: str = None) -> None:
        """
        保存OpenAI配置

        Args:
            config: OpenAI配置字典
            api_key: API密钥（可选，单独存储）
        """
        if api_key:
            await ConfigService.set_setting(ConfigService.KEY_OPENAI_API_KEY, api_key)

        config_slim = {k: v for k, v in config.items() if k != "api_key"}
        await ConfigService.set_setting(
            ConfigService.KEY_OPENAI_CONFIG,
            json.dumps(config_slim)
        )

    @staticmethod
    async def has_soniox_api_key() -> bool:
        """
        检查是否有Soniox API密钥

        Returns:
            是否存在API密钥
        """
        key = await ConfigService.get_setting(ConfigService.KEY_SONIOX_API_KEY)
        return bool(key)

    @staticmethod
    async def has_openai_api_key() -> bool:
        """
        检查是否有OpenAI API密钥

        Returns:
            是否存在API密钥
        """
        key = await ConfigService.get_setting(ConfigService.KEY_OPENAI_API_KEY)
        return bool(key)

    @staticmethod
    async def get_soniox_api_key() -> Optional[str]:
        """
        获取Soniox API密钥

        Returns:
            API密钥，不存在则返回None
        """
        return await ConfigService.get_setting(ConfigService.KEY_SONIOX_API_KEY)

    @staticmethod
    async def get_openai_api_key() -> Optional[str]:
        """
        获取OpenAI API密钥

        Returns:
            API密钥，不存在则返回None
        """
        return await ConfigService.get_setting(ConfigService.KEY_OPENAI_API_KEY)

    @staticmethod
    async def load_openai_config_with_fallback(
        provided_config: OpenAIConfig,
        default_api_url: str = "https://api.openai.com/v1",
        default_model: str = "gpt-4o-mini"
    ) -> OpenAIConfig:
        """
        加载OpenAI配置，如果未提供则从服务器保存中补全

        Args:
            provided_config: 前端提供的配置
            default_api_url: 默认API URL
            default_model: 默认模型

        Returns:
            完整的OpenAIConfig对象
        """
        if provided_config.api_key:
            return provided_config

        # 从服务器保存中获取
        stored_key = await ConfigService.get_openai_api_key()
        if not stored_key:
            return provided_config

        # 加载保存的配置（非密钥部分）
        raw = await ConfigService.get_openai_config() or "{}"
        try:
            base = json.loads(raw) if isinstance(raw, str) else raw
        except Exception:
            base = {}

        return OpenAIConfig(
            api_url=base.get("api_url", provided_config.api_url or default_api_url),
            api_key=stored_key,
            model=base.get("model", provided_config.model or default_model),
        )

    @staticmethod
    async def clear_soniox_api_key() -> None:
        """
        清除Soniox API密钥
        """
        await ConfigService.set_setting(ConfigService.KEY_SONIOX_API_KEY, "")

    @staticmethod
    async def clear_openai_api_key() -> None:
        """
        清除OpenAI API密钥
        """
        await ConfigService.set_setting(ConfigService.KEY_OPENAI_API_KEY, "")

