import marked from 'marked'
import highlightJs from 'highlight.js';
import 'highlight.js/styles/atom-one-dark.css';

export default (value) => {
  if (!value) return
  const rendererMD = new marked.Renderer()
  // 基本设置
  marked.setOptions({
    renderer: rendererMD,
    gfm: true,
    tables: true,
    breaks: false,
    pedantic: false,
    sanitize: false,
    smartLists: true,
    smartypants: false,
    highlight: function(code) {
      return highlightJs.highlightAuto(code).value;
    },
  })
  return marked(value)
}
