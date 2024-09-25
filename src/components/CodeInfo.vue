<template>
  <div class="container">
    <button class="btn btn-primary" @click="copyCode" style="margin-bottom: 20px;">复制代码</button>
    <div ref="editContainer" class="code-editor"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as monaco from 'monaco-editor/esm/vs/editor/editor.main.js';
import JsonWorker from 'monaco-editor/esm/vs/language/json/json.worker?worker';
import { useRoute } from 'vue-router';

// 解决 vite Monaco 提示错误
self.MonacoEnvironment = {
  getWorker() {
    return new JsonWorker();
  },
};

const editContainer = ref(null);
let monacoEditor = null;
let initialLanguage = 'python'; // 默认语言

onMounted(async () => {
  await fetchData(); // 获取代码内容并填充
  window.addEventListener('resize', resizeEditor); // 监听窗口变化
});

// 清理监听器
onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeEditor);
});

// 从后端获取代码内容
const fetchData = async () => {
  const route = useRoute();
  const codeId = route.params.codeId; // 获取codeId

  try {
    const response = await fetch('http://127.0.0.1:8001/code/info', { // 使用完整地址
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ key: codeId }), // 将codeId作为body中的key
    });

    if (!response.ok) {
      throw new Error('网络错误');
    }

    const data = await response.json(); // 解析响应为 JSON
    initialLanguage = data.code_lang; // 获取语言
    createEditor(data.code); // 创建编辑器并填充内容
  } catch (error) {
    console.error('获取代码时出错:', error);
  }
};

const createEditor = (initialValue) => {
  monacoEditor = monaco.editor.create(editContainer.value, {
    value: initialValue,
    readOnly: true,  // 设置为只读
    language: initialLanguage,  // 使用从后端获取的语言
    theme: 'vs-dark',
    selectOnLineNumbers: true,
    renderSideBySide: false,
    colorDecorators: true,
  });

  resizeEditor(); // 初始调整大小
};

// 动态调整编辑器大小
const resizeEditor = () => {
  if (monacoEditor) {
    monacoEditor.layout(); // 重新布局编辑器
  }
};

// 复制代码到剪切板
const copyCode = () => {
  const currentValue = monacoEditor.getValue();
  navigator.clipboard.writeText(currentValue).then(() => {
    alert('代码已复制到剪切板！');
  }).catch(err => {
    console.error('复制代码时出错:', err);
  });
};
</script>

<style scoped>
.container {
  position: relative;
  height: 100vh; /* 使容器占满整个视口 */
  padding-top: 20px; /* 为按钮与上边界留出空隙 */
  box-sizing: border-box; /* 确保padding不会影响高度计算 */
}

.code-editor {
  width: 100%;
  height: calc(100vh - 100px); /* 调整高度，确保不超出窗口范围 */
}
</style>
