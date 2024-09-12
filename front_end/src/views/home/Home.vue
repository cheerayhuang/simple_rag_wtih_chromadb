<template>
    <div class="mainPage">
        <div class="chatContent">
            <div class="top" id="chatArea">
                <div id="messageWindowId">
                    <!--<div v-if='questionList' class="question">-->
                    <!--<div v-for="(item, index) in questionList" :key="index">-->
                    <!--<span class="question_span">{{item}}</span>-->
                    <!--</div>-->
                    <!--</div>-->

                    <div v-if='question_new' class="question">
                        <span class="question_span">{{question_new}}</span>
                    </div>
                    <div v-if="isWaiting">正在回答。。。</div>
                    <div v-if='responseData' class="answer">
                        <div class="response">{{responseData}}</div>
                    </div>
                </div>
            </div>
            <div class="fileupload">
                <el-upload
                        class="upload-demo"
                        action="http://localhost:8000/collections/langchain/documents/"
                        :limit="1"
                        :on-success="handleUploadSuccess"
                        :file-list="fileList">
                    <el-button size="small" type="primary">点击上传</el-button>
                    <div slot="tip" class="el-upload__tip">只能上传txt文件</div>
                </el-upload>
            </div>

            <div class="sendArea">
                <input type="text" placeholder='说点什么吧~' @change="handleQuestionChange" v-model="question"
                       @keyup.enter="sendData"/>
                <button @click="sendData">
                    <img src="../../assets/sendIcon.svg"/>
                    发送
                </button>
            </div>
        </div>

    </div>


</template>

<script>


    import axios from 'axios'

    export default {
        name: "Home",

        data() {
            return {
                file: null,
                question: '',
                responseData: '',
                question_new: '',
                fileList: [],
                isWaiting: false,
                chatIsOver: true
                // questionList: [],
                // responseList: []
            };
        },
        methods: {
            handleUploadSuccess(res, file) {
                this.$message({
                    message: '文件上传成功',
                    type: 'success'
                });
            },
            handleQuestionChange() {
                console.log(this.question)
            },
            async sendData() {
                if (!this.chatIsOver) {
                    this.$message({
                        message: '有对话进行中！',
                        type: 'warning'
                    });
                    return;
                }
                this.responseData = '';
                this.isWaiting = true;
                this.chatIsOver = false;
                this.question_new = this.question;

                const my_params = {
                    input: this.question_new,
                    parameters: {},
                    collection: 'langchain',
                };
                console.log(my_params)
                try {
                    const response = await axios.post('http://localhost:8000/llm', my_params);
                    // 处理响应
                    console.log(response.data);
                    this.isWaiting = false;
                    this.responseData = response.data.data;
                    this.chatIsOver = true;
                } catch (error) {
                    // 处理错误
                    console.error(error);
                }
            }
        }
    }


</script>

<style scoped>
    .mainPage {
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        padding: 0 60px 24px;
        height: 100%;
        overflow: hidden;
        position: relative;
        min-width: 1280px;
        max-width: 1920px;
        margin: 0 auto;
    }

    .chatContent {
        position: relative;
        display: flex;
        justify-content: flex-start;
        flex-direction: column;
        flex-grow: 1;
        margin-right: 40px;
        height: calc(100% - 24px);
        overflow-y: hidden;
        padding: 32px 0 0 0;
        box-sizing: border-box;
    }

    .top {
        height: calc(100% - 110px);
        overflow-y: auto;
        margin-bottom: 40px;
    }

    .sendArea {
        display: flex;
        width: 100%;
        box-sizing: border-box;
        padding: 10px 12px 10px 24px;
        justify-content: space-between;
        align-items: center;
        border-radius: 8px;
        border: 2px solid #464A53;
        background: #FFF;
        position: relative;

    }

    input {
        height: 36px;
        line-height: 36px;
        flex-grow: 1;
        border: 0;
        outline: 0;
    }


    .question {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 40px;
    }

    .question_span {
        padding: 12px 20px;
        color: #121316;
        font-size: 14px;
        line-height: 24px;
        border-radius: 8px;
        background: #dff8ff;
        max-width: 93.75%;
    }

    .answer {
        border-radius: 8px;
        background: rgba(33, 38, 192, 0.10);
        padding: 12px;
    }

    .response {
        color: #121316;
        font-size: 14px;
        line-height: 24px;
        padding: 18px 42px;
    }
    .fileupload{
        width: 200px;
    }

</style>
