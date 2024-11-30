# LICENSE HEADER MANAGED BY add-license-header
#
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2024 @ SYNTROPIX-AI.org. All Rights Reserved. ===========
#

from .function_schema import get_openai_tool_schema
from .image import image2base64, is_url, parse_image
from .macros import (
    ASYNC_GET_FINAL_MESSAGE,
    CALL_ASYNC_CALLBACK,
    FORMAT_PROMPT,
    GET_FINAL_MESSAGE,
    STR_TO_USERMESSAGE,
    UPDATE_SYSTEM,
)
from .yaml_loader import YAMLLoader


__all__ = [
    "get_openai_tool_schema",
    "YAMLLoader",
    "is_url",
    "image2base64",
    "parse_image",
    "FORMAT_PROMPT",
    "UPDATE_SYSTEM",
    "STR_TO_USERMESSAGE",
    "GET_FINAL_MESSAGE",
    "ASYNC_GET_FINAL_MESSAGE",
    "CALL_ASYNC_CALLBACK",
]
