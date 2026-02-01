from main import main


def handler(event, context):  # noqa: ANN001, ANN201
    main()
    return {"status": "ok"}
