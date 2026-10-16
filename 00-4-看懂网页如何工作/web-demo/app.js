// JavaScript 是网页的"行为":决定点击之后发生什么。
// 以 // 开头的是注释,给人看的,浏览器会忽略。
// 整段程序的意思:点击按钮 → 向服务器要 message.json → 把里面的消息显示在页面上。

// 按名牌(id)找到页面上的按钮和结果那一段,分别存进两个变量
const button = document.querySelector("#load-message"); // 找到 id 是 load-message 的按钮
const result = document.querySelector("#result"); // 找到 id 是 result 的那一段文字

// 给按钮设置"监听":一旦被点击(click),就执行后面花括号里的操作
button.addEventListener("click", async () => {
  result.textContent = "正在请求…"; // 先在页面上显示"正在请求…"

  // try / catch:先尝试执行 try 里的步骤;如果出错,就跳到 catch 里处理
  try {
    // ↓↓↓ 任务要求:不要修改这一行(这就是浏览器向服务器发出的 HTTP 请求)↓↓↓
    const response = await fetch("message.json"); // 向服务器请求 message.json;await = 等服务器回复

    // 服务器回复了,但状态码不是成功(2xx),例如 404 = 找不到文件
    if (!response.ok) {
      result.textContent = `请求失败：服务器返回了状态码 ${response.status}。请在 Network 里点开 message.json，查看 Status 和 Response。`;
      return; // 到此结束,不再往下执行
    }

    const data = await response.json(); // 把回复的内容当作 JSON 读出来,存进 data
    result.textContent = data.message; // 取出 data 里标签为 message 的内容,显示在页面上
  } catch (error) {
    // 请求失败时走到这里。根据错误类型,给出不同的排查方向
    if (error instanceof SyntaxError) {
      // 收到了回复,但内容不是合法的 JSON
      result.textContent = "请求失败：收到了回复，但内容不是合法的 JSON。请在 Network 里点开 message.json，查看 Response 里返回了什么。";
    } else {
      // 请求没有成功发出去,或被浏览器拦截
      result.textContent = "请求失败：请求没有成功发出，或被浏览器拦截。请按 F12，先看 Console 里的红色报错，再看 Network 里这次请求的状态。";
    }
    console.error(error); // 把错误详情打印到开发者工具的 Console 标签
  }
});
