# -*- coding: utf-8 -*-
import os

html = '''<!DOCTYPE html>
<html lang=\"zh-CN\">
<head>
<meta charset=\"UTF-8\">
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>\u552e\u540e\u5de5\u5355\u667a\u80fd\u5904\u7406\u7cfb\u7edf</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#f5f7fa;color:#1e293b}
nav{background:#fff;border-bottom:1px solid #e2e8f0;padding:0 24px;position:sticky;top:0;z-index:50}
.nav-inner{max-width:1200px;margin:0 auto;display:flex;align-items:center;height:60px;gap:32px}
.nav-logo{font-weight:700;font-size:18px;color:#0d9488;text-decoration:none}
.nav-links{display:flex;gap:20px;margin-left:auto}
.nav-links a{text-decoration:none;color:#475569;font-size:14px;font-weight:500}
.nav-links a:hover{color:#0d9488}
.nav-links .btn-nav{background:#0d9488;color:#fff;padding:6px 18px;border-radius:6px;font-size:13px;text-decoration:none}
.hero{background:linear-gradient(135deg,#f0fdf4,#ecfeff,#f0f9ff);padding:80px 24px 60px;text-align:center}
.hero h1{font-size:44px;font-weight:800;color:#0f172a;margin-bottom:16px}
.hero h1 span{color:#0d9488}
.hero p{font-size:18px;color:#475569;max-width:640px;margin:0 auto 32px}
.hero-actions{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.btn{display:inline-flex;padding:12px 28px;border-radius:8px;font-size:15px;font-weight:600;text-decoration:none;cursor:pointer;border:none}
.btn-primary{background:#0d9488;color:#fff}
.btn-primary:hover{background:#0f766e;transform:translateY(-1px)}
.btn-outline{background:#fff;color:#334155;border:1.5px solid #cbd5e1}
.stats{display:flex;justify-content:center;gap:40px;padding:40px 24px;max-width:900px;margin:-30px auto 0;background:#fff;border-radius:12px;flex-wrap:wrap}
.stat-item{text-align:center;min-width:120px}
.stat-num{font-size:32px;font-weight:800;color:#0d9488}
.stat-label{font-size:13px;color:#64748b}
.section{padding:64px 24px;max-width:1100px;margin:0 auto}
.section h2{font-size:30px;font-weight:700;text-align:center;margin-bottom:48px;color:#0f172a}
.flow{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;margin-bottom:40px}
.flow-node{background:#fff;border:1.5px solid #e2e8f0;border-radius:10px;padding:12px 14px;text-align:center;min-width:80px}
.flow-node .icon{font-size:20px;display:block;margin-bottom:2px}
.flow-node .name{font-size:11px;font-weight:600}
.flow-node.highlight{border-color:#0d9488;background:#f0fdf4}
.flow-arrow{font-size:16px;color:#94a3b8;margin:0 3px}
.flow-sub{text-align:center;font-size:11px;color:#94a3b8;margin-top:4px}
.card{background:#fff;border-radius:12px;padding:24px;border:1px solid #e2e8f0}
.card h3{font-size:16px;font-weight:600;margin-bottom:8px}
.card p{font-size:14px;color:#64748b;line-height:1.6}
.cta{background:#0d9488;padding:60px 24px;text-align:center;color:#fff}
.cta h2{font-size:28px;font-weight:700;margin-bottom:12px}
.cta p{font-size:16px;margin-bottom:24px;max-width:500px;margin:0 auto 24px}
.cta .btn{background:#fff;color:#0d9488}
footer{background:#0f172a;color:#94a3b8;padding:32px 24px;text-align:center;font-size:14px}
footer a{color:#5eead4;text-decoration:none}
</style></head>
<body>
<nav><div class=\"nav-inner\"><a href=\"/\" class=\"nav-logo\">\u552e\u540e\u5de5\u5355\u667a\u80fd\u5904\u7406\u7cfb\u7edf</a><div class=\"nav-links\"><a href=\"/demo\" class=\"btn-nav\">\u4f53\u9a8c Demo</a><a href=\"/review\" class=\"btn-nav\">\u5ba1\u6838\u9762\u677f</a></div></div></nav>

<section class=\"hero\">
<div><div style=\"display:inline-block;background:#d1fae5;color:#065f46;font-size:13px;font-weight:600;padding:4px 14px;border-radius:20px;margin-bottom:20px\">AI + RPA \u81ea\u52a8\u5316\u65b9\u6848</div>
<h1>\u552e\u540e\u5904\u7406\u6548\u7387\u63d0\u5347 <span>10-15 \u500d</span></h1>
<p>\u4f20\u7edf\u4eba\u5de5\u5904\u7406\u6bcf\u5355\u7ea6 10-15 \u5206\u949f\uff0c\u7cfb\u7edf\u81ea\u52a8\u5904\u7406\u5e73\u5747 30 \u79d2\u5b8c\u6210\uff0c\u5305\u542b\u610f\u56fe\u8bc6\u522b\u3001\u8ba2\u5355\u67e5\u8be2\u3001\u51b3\u7b56\u5224\u5b9a\u3001\u9000\u6b3e\u6267\u884c\u3001\u56de\u590d\u751f\u6210\u5168\u6d41\u7a0b\u3002</p>
<div class=\"hero-actions\"><a href=\"/demo\" class=\"btn btn-primary\">\u4f53\u9a8c Demo</a><a href=\"/review\" class=\"btn btn-outline\">\u5ba1\u6838\u9762\u677f</a></div>
</div></section>

<div class=\"stats\">
<div class=\"stat-item\"><div class=\"stat-num\">7</div><div class=\"stat-label\">Demo \u573a\u666f</div></div>
<div class=\"stat-item\"><div class=\"stat-num\">&lt;30\u79d2</div><div class=\"stat-label\">\u5e73\u5747\u5904\u7406\u65f6\u95f4</div></div>
<div class=\"stat-item\"><div class=\"stat-num\">~70%</div><div class=\"stat-label\">\u81ea\u52a8\u5904\u7406\u6bd4\u4f8b</div></div>
<div class=\"stat-item\"><div class=\"stat-num\">24/7</div><div class=\"stat-label\">\u5168\u5929\u5019\u8fd0\u884c</div></div>
</div>

<section class=\"section\">
<h2>\u5de5\u4f5c\u539f\u7406</h2>
<p style=\"text-align:center;color:#64748b;font-size:16px;margin:-36px auto 48px;max-width:560px\">\u7cfb\u7edf\u901a\u8fc7\u4e00\u4e32\u81ea\u52a8\u5316\u6b65\u9aa4\u5b8c\u6210\u552e\u540e\u5904\u7406\uff0c\u6bcf\u4e2a\u73af\u8282\u7684\u51b3\u7b56\u90fd\u662f\u53ef\u89e3\u91ca\u7684</p>

<div class=\"flow\">
<div class=\"flow-node highlight\"><span class=\"icon\">\U0001F4AC</span><span class=\"name\">\u5ba2\u6237\u6d88\u606f</span></div>
<span class=\"flow-arrow\">\u2192</span>
<div class=\"flow-node\"><span class=\"icon\">\U0001F9E0</span><span class=\"name\">\u610f\u56fe\u5206\u7c7b</span></div>
<div class=\"flow-sub\">LLM / \u5173\u952e\u8bcd\u5339\u914d</div>
<span class=\"flow-arrow\">\u2192</span>
<div class=\"flow-node\"><span class=\"icon\">\U0001F50D</span><span class=\"name\">\u8ba2\u5355\u67e5\u8be2</span></div>
<div class=\"flow-sub\">Shopify API / 17Track</div>
<span class=\"flow-arrow\">\u2193</span>
<div style=\"display:flex;gap:0;align-items:center\">
<div class=\"flow-node\" style=\"border-color:#f59e0b;background:#fffbeb\"><span class=\"icon\">\U0001F916</span><span class=\"name\">RPA \u5146\u5e95</span></div>
<div class=\"flow-sub\">API \u5931\u8d25\u65f6\u89e6\u53d1</div>
</div>
<span class=\"flow-arrow\">\u2192</span>
<div class=\"flow-node\" style=\"border-color:#0d9488;background:#f0fdf4\"><span class=\"icon\">\u2696\uFE0F</span><span class=\"name\">\u51b3\u7b56\u5f15\u64ce</span></div>
<div class=\"flow-sub\">\u51b3\u7b56\u89c4\u5219\uff1a\u91d1\u989d &lt; \u2192 \u81ea\u52a8\u9000\u6b3e<br>\u7269\u6d41\u505c\u6ede &gt;10\u5929 \u2192 \u90e8\u5206\u9000\u6b3e<br>\u91d1\u989d &gt; \u2192 \u4eba\u5de5\u5ba1\u6838</div>
</div>'''

# More content
html2 = '''
<div style=\"display:flex;gap:20px;margin-top:40px;flex-wrap:wrap\">
<div class=\"card\" style=\"flex:1;min-width:200px\"><h3>1. \u610f\u56fe\u8bc6\u522b</h3><p>\u7cfb\u7edf\u81ea\u52a8\u5206\u6790\u5ba2\u6237\u6d88\u606f\uff0c\u5224\u65ad\u5c5e\u4e8e\u9000\u6b3e\u3001\u8ba2\u5355\u5f02\u5e38\u8fd8\u662f\u552e\u540e\u95ee\u9898\uff0c\u540c\u65f6\u63d0\u53d6\u8ba2\u5355\u53f7\u3002</p></div>
<div class=\"card\" style=\"flex:1;min-width:200px\"><h3>2. \u6570\u636e\u67e5\u8be2</h3><p>\u901a\u8fc7 Shopify API \u83b7\u53d6\u8ba2\u5355\u8be6\u60c5\u300117Track \u67e5\u8be2\u7269\u6d41\u8ddf\u8e2a\u3002\u63a5\u53e3\u5931\u8d25\u65f6\u81ea\u52a8\u5207\u6362\u5230 RPA \u6d4f\u89c8\u5668\u6293\u53d6\u3002</p></div>
<div class=\"card\" style=\"flex:1;min-width:200px\"><h3>3. \u89c4\u5219\u5224\u5b9a</h3><p>\u6839\u636e\u91d1\u989d\u3001\u7269\u6d41\u72b6\u6001\u3001\u98ce\u9669\u7b49\u7ea7\u7efc\u5408\u5224\u5b9a\u5904\u7406\u65b9\u5f0f\uff1a\u81ea\u52a8\u9000\u6b3e\u3001\u90e8\u5206\u9000\u6b3e\u6216\u8f6c\u4eba\u5de5\u5ba1\u6838\u3002</p></div>
<div class=\"card\" style=\"flex:1;min-width:200px\"><h3>4. \u6267\u884c\u56de\u590d</h3><p>\u81ea\u52a8\u6267\u884c\u9000\u6b3e\u64cd\u4f5c\uff08Shopify API\uff09\uff0c\u751f\u6210\u5ba2\u6237\u56de\u590d\u5185\u5bb9\uff0c\u65e0\u9700\u4eba\u5de5\u5e72\u9884\u3002</p></div>
</div>
</section>

<section style=\"background:#fff;padding:64px 24px\">
<div style=\"max-width:1100px;margin:0 auto\">
<h2>7 \u4e2a Demo \u573a\u666f\u6d4b\u8bd5</h2>
<p style=\"text-align:center;color:#64748b;font-size:16px;margin:-36px auto 48px;max-width:560px\">\u4ee5\u4e0b\u573a\u666f\u5747\u53ef\u5728 Demo \u9875\u9762\u4e2d\u9009\u62e9\u5e76\u5b9e\u9645\u8fd0\u884c\u67e5\u770b\u7ed3\u679c</p>
<div style=\"display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr))\">
<div style=\"background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:14px 16px;font-size:13px\"><strong>\u81ea\u52a8\u5168\u989d\u9000\u6b3e</strong><br>\u8ba2\u5355\u672a\u6536\u5230 + \u91d1\u989d&lt; \u2192 \u81ea\u52a8\u5168\u989d\u9000\u6b3e</div>
<div style=\"background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:14px 16px;font-size:13px\"><strong>\u81ea\u52a8\u90e8\u5206\u9000\u6b3e</strong><br>\u7269\u6d41\u5361\u4f4f 12\u5929 \u2192 50% \u90e8\u5206\u9000\u6b3e</div>
<div style=\"background:#fef3c7;border:1px solid #fde68a;border-radius:8px;padding:14px 16px;font-size:13px\"><strong>\u8f6c\u4eba\u5de5\u5ba1\u6838</strong><br>\u91d1\u989d &gt; + \u5df2\u9001\u8fbe\u4e89\u8bae \u2192 \u81ea\u52a8\u8bc6\u522b\u9ad8\u98ce\u9669\u5e76\u63d0\u4ea4\u5ba1\u6838</div>
<div style=\"background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:14px 16px;font-size:13px\"><strong>RPA \u5146\u5e95\u81ea\u52a8\u9000\u6b3e</strong><br>API \u67e5\u4e0d\u5230\u7269\u6d41 \u2192 RPA \u6d4f\u89c8\u5668\u6293\u53d6 \u2192 \u786e\u8ba4\u4e22\u5931\u540e\u81ea\u52a8\u9000\u6b3e</div>
</div>
<div style=\"text-align:center;margin-top:24px\"><a href=\"/demo\" class=\"btn btn-primary\">\u67e5\u770b\u6240\u6709 7 \u4e2a\u573a\u666f</a></div>
</div>
</section>

<section class=\"cta\">
<h2>\u5f00\u59cb\u4f53\u9a8c</h2>
<p>\u6253\u5f00 Demo \u9875\u9762\uff0c\u9009\u62e9\u4e00\u4e2a\u573a\u666f\uff0c\u67e5\u770b\u7cfb\u7edf\u5982\u4f55\u81ea\u52a8\u5904\u7406\u552e\u540e\u5de5\u5355\u3002</p>
<a href=\"/demo\" class=\"btn\">\u8fdb\u5165 Demo</a>
<a href=\"/review\" class=\"btn\" style=\"background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.4);margin-left:12px\">\u5ba1\u6838\u9762\u677f</a>
</section>

<footer><p>\u552e\u540e\u5de5\u5355\u667a\u80fd\u5904\u7406\u7cfb\u7edf &middot; AI Agent + RPA \u6df7\u5408\u67b6\u6784</p></footer>
</body></html>
'''

path = r"C:/Users/winni/Aftersale_system/web/templates/showcase.html"
with open(path, \"w\", encoding=\"utf-8\") as f:
    f.write(html + html2)
print(\"Written\", os.path.getsize(path), \"bytes\")