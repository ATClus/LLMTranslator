import logging
import os
from dotenv import load_dotenv
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class LMStudioLocalAPI:
    LMSTUDIO_API_URL = os.getenv("LMSTUDIO_API_URL")
    MODEL_ID = os.getenv("MODEL_ID")
    CONTENT_TYPE_JSON = "application/json"

    def __init__(self, base_url=LMSTUDIO_API_URL):
        self.base_url = base_url
        self.headers = {
            "Content-Type": self.CONTENT_TYPE_JSON
        }
        logger.info(f"LMStudioLocalAPI initialized with URL: {self.LMSTUDIO_API_URL} and model: {self.MODEL_ID}")

    def conn_test(self, text, system_prompt=""):
        try:
            request_body = {
                "model": self.MODEL_ID,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                "temperature": 0.1,
                "max_tokens": -1,
                "stream": False
            }
            logger.info(f"Sending request with prompt: {text[:50]}...")
            response = requests.post(self.LMSTUDIO_API_URL, headers=self.headers, json=request_body)

            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response preview: {response.text[:200]}...")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            logger.error(f"Error in LMStudioLocalAPI: {err}")
            return None
        except requests.exceptions.RequestException as err:
            logger.error(f"Error in LMStudioLocalAPI: {err}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None

    def translate(self, text,
                  system_prompt="Translate the following English text into Brazilian Portuguese. Instructions: - Use a colloquial, natural tone appropriate for speech in a TV series - Preserve any formatting tags like <b>, <i>, etc. - Return ONLY the translated text, nothing else"):
        try:
            request_body = {
                "model": self.MODEL_ID,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                "temperature": 0.1,
                "max_tokens": -1,
                "stream": False
            }
            response = requests.post(self.LMSTUDIO_API_URL, headers=self.headers, json=request_body)
            response.raise_for_status()
            result = response.json()

            if result and "choices" in result and len(result["choices"]) > 0:
                if "message" in result["choices"][0]:
                    return result["choices"][0]["message"]["content"].strip()
                elif "text" in result["choices"][0]:
                    return result["choices"][0]["text"].strip()
                else:
                    logger.warning("Unexpected response format")
                    logger.info(f"Response: {result}")
                    return ""
            else:
                logger.warning("No choices found in the response")
                return ""
        except requests.exceptions.HTTPError as err:
            logger.error(f"Error in LMStudioLocalAPI: {err}")
            return None
        except requests.exceptions.RequestException as err:
            logger.error(f"Error in LMStudioLocalAPI: {err}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
