STORAGE_PATH="browser-auth-data.json"

uv run playwright open https://huggingface.co/login --load-storage ${STORAGE_PATH} --save-storage ${STORAGE_PATH}
uv run playwright open https://github.com/login --load-storage ${STORAGE_PATH} --save-storage ${STORAGE_PATH}
uv run playwright open https://www.linkedin.com/login --load-storage ${STORAGE_PATH} --save-storage ${STORAGE_PATH}
uv run playwright open https://www.x.com --load-storage ${STORAGE_PATH} --save-storage ${STORAGE_PATH}
