def application(environ, start_response):
    # Получаем параметры GET и POST
    query_string = environ.get('QUERY_STRING', '')
    post_data = environ.get('wsgi.input').read()

    # Преобразуем данные в словарь
    get_params = dict(qc.split('=') for qc in query_string.split('&'))
    post_params = dict(p.split('=') for p in post_data.decode().split('&'))

    # Формируем ответ
    response_body = f"GET параметры: {get_params}\nPOST параметры: {post_params}"
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]

    # Отправляем ответ клиенту
    start_response(status, response_headers)
    return [response_body.encode()]
