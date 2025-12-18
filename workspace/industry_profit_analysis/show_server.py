import http.server
import socketserver
import webbrowser
import threading
import os

# 切换到当前目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 定义服务器端口
PORT = 8000

# 创建处理器
Handler = http.server.SimpleHTTPRequestHandler

# 创建服务器
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"服务器启动，地址: http://localhost:{PORT}")
    
    # 在新线程中自动打开浏览器
    def open_browser():
        webbrowser.open(f'http://localhost:{PORT}/二级市场板块回报分析.html')
    
    # 等待1秒后打开浏览器
    timer = threading.Timer(1.0, open_browser)
    timer.daemon = True
    timer.start()
    
    try:
        print("按 Ctrl+C 停止服务器")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")