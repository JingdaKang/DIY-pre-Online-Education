import { Message } from 'element-ui'
export default {
  /**
   * 传入时间戳，转换指定的时间格式
   * @param {Number} val      时间戳
   * @param {String} dateType 要得到的时间格式 例如 YYYY-MM-DD hh:mm:ss
   * @return dataStr 例如 YYYY-MM-DD hh:mm:ss
   */
  switchTime: (val = +new Date(), dateType = 'YYYY-MM-DD hh:mm:ss') => {
    // 将字符串转换成数字
    const timeStamp = +new Date(val)

    // 如果转换成数字出错
    if (!timeStamp) {
      return val
    }
    let str
    // 得到时间字符串
    const dateStr = new Date(timeStamp)
    str = dateType.replace('YYYY', dateStr.getFullYear())
    str = str.replace('MM', (dateStr.getMonth() + 1 < 10 ? '0' : '') + (dateStr.getMonth() + 1))
    str = str.replace('DD', (dateStr.getDate() < 10 ? '0' : '') + dateStr.getDate())
    str = str.replace('hh', (dateStr.getHours() < 10 ? '0' : '') + dateStr.getHours())
    str = str.replace('mm', (dateStr.getMinutes() < 10 ? '0' : '') + dateStr.getMinutes())
    str = str.replace('ss', (dateStr.getSeconds() < 10 ? '0' : '') + dateStr.getSeconds())

    return str
  },
  /**
   * 时间显示
   */
  timeView: function (val) {
    const now = +new Date() // 当时时间
    const timeStamp = +new Date(val) // 需要处理的时间
    const result = now - timeStamp // 相差的时间戳
    const min = 60 * 1000 // 分钟的毫秒数
    const hour = 60 * 60 * 1000 // 小时的毫秒数
    const day = 60 * 60 * 1000 * 24 // 日的毫秒数
    if (result / min < 1) {
      return '刚刚发布'
    } else if (result / min < 60) {
      return Math.floor(result / min) + '分钟前'
    } else if (result / hour > 1 && result / hour < 24) {
      return Math.floor(result / hour) + '小时前'
    } else if (result / day > 1 && result / day < 7) {
      return Math.floor(result / day) + '天前'
    } else if (this.switchTime(now, 'YYYY') === this.switchTime(timeStamp, 'YYYY')) {
      return this.switchTime(timeStamp, 'MM月DD日')
    } else {
      return this.switchTime(timeStamp, 'YYYY年MM月DD日')
    }
  },
}
