# python3.10のイメージをダウンロード
FROM python:3.10-buster
ENV PYTHONUNBUFFRED=1

WORKDIR /src

# pipを使ってpoetryをインストール
RUN pip install poetry

# poetryの定義ファイルをコピー(存在する場合)
COPY pyproject.toml* poetry.lock* ./

# poetryでライブラリをインストール(pyproject.tomlがすでにある場合)
RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

# uvicornのサーバーを立ち上げる
ENTRYPOINT [ "poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload" ]