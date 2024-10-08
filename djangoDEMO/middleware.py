# middleware.py
class SavePreviousUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 檢查 `previous_url` 是否已經存在於 session 中
        if 'previous_url' in request.session:
            # 儲存當前的 previous_url
            request.previous_url = request.session['previous_url']
        else:
            request.previous_url = None
        
        # 檢查是否為 AJAX 請求
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        # 儲存目前的 URL 到 session 中（但排除 AJAX 和管理後台）
        if not is_ajax and not request.path.startswith('/admin/'):
            request.session['previous_url'] = request.build_absolute_uri()

        response = self.get_response(request)
        return response