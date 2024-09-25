<template>
  <div class="container">
    <div class="form-group" style="width: 33.33%; margin-bottom: 10px;">
      <label for="languageSelect" style="color: white">请选择代码语言</label>
      <select id="languageSelect" v-model="selectedLanguage" class="form-control" @change="changeLanguage" style="background-color: #1E1E1E; color: white">
        <option value="python">Python</option>
        <option value="text">Text</option>
        <option value="json">JSON</option>
        <option value="java">Java</option>
      </select>
    </div>
    <div ref="editContainer" class="code-editor"></div>
    <button class="btn btn-primary" style="position: absolute; bottom: 20px; right: 20px;" @click="saveCode">保存代码</button>

    <!-- Bootstrap 模态框 -->
    <div class="modal fade" id="successModal" tabindex="-1" aria-labelledby="modalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="modalLabel">保存成功</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body text-center">
            <span>请务必牢记如下地址，如果遗忘将不可找回</span><br/>
            <span>链接有效期24小时</span><br/>
            <span><a :href="responseUrl" target="_blank">{{ responseUrl }}</a></span><br/>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal">确定</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import * as monaco from 'monaco-editor/esm/vs/editor/editor.main.js';
import JsonWorker from 'monaco-editor/esm/vs/language/json/json.worker?worker';
import { Modal } from 'bootstrap';

self.MonacoEnvironment = {
  getWorker() {
    return new JsonWorker();
  },
};

const editContainer = ref(null);
let monacoEditor = null;
const selectedLanguage = ref('python');
const responseUrl = ref(''); // 存放响应的 URL

onMounted(() => {
  createEditor(selectedLanguage.value);
  window.addEventListener('resize', resizeEditor);
});

watch(
  () => selectedLanguage.value,
  () => {
    const currentValue = monacoEditor.getValue();
    monacoEditor.setValue(currentValue);
    monaco.editor.setModelLanguage(monacoEditor.getModel(), selectedLanguage.value);
  }
);

const createEditor = (language) => {
  monacoEditor = monaco.editor.create(editContainer.value, {
    value: '',
    language,
    theme: 'vs-dark',
    selectOnLineNumbers: true,
    renderSideBySide: false,
    colorDecorators: true,
  });
  resizeEditor();
};

const resizeEditor = () => {
  if (monacoEditor) {
    monacoEditor.layout();
  }
};

const saveCode = async () => {
  const currentCode = monacoEditor.getValue();
  const payload = {
    code: currentCode,
    code_lang: selectedLanguage.value,
  };

  try {
    const response = await fetch('http://127.0.0.1:8001/code/save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error('网络错误');
    }
    const data = await response.json();
    responseUrl.value = data.url; // 获取后端返回的 URL

    // 使用导入的 Modal 组件
    const modalElement = document.getElementById('successModal');
    const modalInstance = new Modal(modalElement);
    modalInstance.show(); // 显示模态框
  } catch (error) {
    console.error('保存代码时出错:', error);
    alert('保存代码失败！');
  }
};
</script>

<style scoped>
.container {
  position: relative;
  height: 100vh;
}

.code-editor {
  width: 100%;
  height: calc(100vh - 150px);
}
</style>
