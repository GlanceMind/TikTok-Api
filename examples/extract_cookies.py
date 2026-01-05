#!/usr/bin/env python3
"""
TikTok Cookies Extractor Helper
帮助从浏览器提取完整的 TikTok cookies
"""

import json

def main():
    print("=" * 70)
    print("TikTok Cookies 提取助手")
    print("=" * 70)
    print("\n请按以下步骤操作：\n")
    
    print("步骤 1: 打开浏览器访问 https://www.tiktok.com")
    print("步骤 2: 按 F12 打开开发者工具")
    print("步骤 3: 点击 'Console' 或'控制台' 标签")
    print("步骤 4: 复制并粘贴以下 JavaScript 代码到控制台，然后按回车：\n")
    
    js_code = """
// 复制以下所有代码到浏览器Console
let cookies = {};
document.cookie.split('; ').forEach(cookie => {
    const [name, value] = cookie.split('=');
    cookies[name] = value;
});
console.log(JSON.stringify(cookies, null, 2));
copy(JSON.stringify(cookies, null, 2));
console.log("\\n✓ Cookies 已复制到剪贴板！");
"""
    
    print("─" * 70)
    print(js_code)
    print("─" * 70)
    
    print("\n步骤 5: 代码执行后，cookies JSON 将自动复制到剪贴板")
    print("步骤 6: 粘贴 cookies 到下面，然后按两次回车（输入空行）结束:\n")
    
    try:
        print("粘贴 cookies JSON（粘贴后按两次回车）:")
        print("─" * 70)
        
        # 读取多行输入直到遇到空行
        lines = []
        while True:
            try:
                line = input()
                if not line.strip():  # 空行，结束输入
                    break
                lines.append(line)
            except EOFError:
                break
        
        cookies_json = '\n'.join(lines)
        
        if not cookies_json.strip():
            print("\n✗ 错误：没有输入任何内容")
            return
        
        print("─" * 70)
        print(f"\n正在解析 {len(lines)} 行 JSON...")
        
        cookies = json.loads(cookies_json)
        
        print(f"\n✓ 成功解析！找到 {len(cookies)} 个 cookies")
        print("\n关键 cookies:")
        
        important_cookies = ['msToken', 'ttwid', 'tt_csrf_token', 'odin_tt', 'sid_tt', 'sessionid', 'sid_ucp_v1']
        for key in important_cookies:
            if key in cookies:
                value = cookies[key]
                display_value = value[:20] + "..." if len(value) > 20 else value
                print(f"  ✓ {key}: {display_value}")
            else:
                print(f"  ⚠ {key}: 缺失")
        
        # Save to file
        output_file = "tiktok_cookies.json"
        with open(output_file, "w") as f:
            json.dump(cookies, f, indent=2)
        
        print(f"\n✓ Cookies 已保存到: {output_file}")
        print(f"\n现在可以使用这些 cookies 运行脚本了！")
        
        # Show usage
        print("\n" + "=" * 70)
        print("如何使用这些 cookies:")
        print("=" * 70)
        print("\n在你的脚本中：")
        print("""
import json

# 加载 cookies
with open('tiktok_cookies.json', 'r') as f:
    cookies = json.load(f)

# 使用 cookies 创建 session
await api.create_sessions(
    cookies=[cookies],  # 传递完整 cookies
    num_sessions=1,
    proxies=[proxy_config],
    browser="webkit",
    headless=True,
)
""")
        
    except json.JSONDecodeError as e:
        print(f"\n✗ JSON 解析错误: {e}")
        print("请确保粘贴的是有效的 JSON 格式")
    except KeyboardInterrupt:
        print("\n\n已取消")
    except Exception as e:
        print(f"\n✗ 错误: {e}")

if __name__ == "__main__":
    main()
