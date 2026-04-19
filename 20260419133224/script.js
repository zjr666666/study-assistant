/**
 * =====================================================
 *  专注时长统计 - JavaScript 逻辑
 *  =====================================================
 *  功能: 计时器、专注模式、数据统计、本地存储
 */

// ==================== DOM 元素引用 ====================
const timerDisplay = document.getElementById('timerDisplay');
const statusBadge = document.getElementById('statusBadge');
const statusText = document.getElementById('statusText');
const goalBtns = document.querySelectorAll('.goal-btn');
const controlBtn = document.getElementById('controlBtn');
const focusWarning = document.getElementById('focusWarning');
const warningCount = document.getElementById('warningCount');
const continueBtn = document.getElementById('continueBtn');
const giveUpBtn = document.getElementById('giveUpBtn');
const todayTime = document.getElementById('todayTime');
const weekTime = document.getElementById('weekTime');
const sessionCount = document.getElementById('sessionCount');
const weekChart = document.getElementById('weekChart');
const chartLabels = document.getElementById('chartLabels');
const historyList = document.getElementById('historyList');
const clearBtn = document.getElementById('clearBtn');
const toast = document.getElementById('toast');
const toastIcon = document.getElementById('toastIcon');
const toastMessage = document.getElementById('toastMessage');

// ==================== 状态变量 ====================
let isFocusing = false;           // 是否正在专注
let focusStartTime = null;        // 专注开始时间
let elapsedSeconds = 0;           // 已专注秒数
let timerInterval = null;         // 计时器interval
let currentGoal = 25;             // 当前目标（分钟）
let distractionCount = 0;         // 分心次数

// ==================== 常量定义 ====================
const STORAGE_KEY = 'focus_timer_data';
const WEEKDAYS = ['日', '一', '二', '三', '四', '五', '六'];

// ==================== 本地存储 ====================

/**
 * 获取所有专注记录
 */
function getRecords() {
    try {
        const data = localStorage.getItem(STORAGE_KEY);
        return data ? JSON.parse(data) : [];
    } catch (e) {
        console.error('读取数据失败:', e);
        return [];
    }
}

/**
 * 保存专注记录
 */
function saveRecords(records) {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(records));
    } catch (e) {
        console.error('保存数据失败:', e);
    }
}

/**
 * 添加一条专注记录
 */
function addRecord(duration, goal) {
    const records = getRecords();
    const now = new Date();
    
    records.push({
        date: now.toISOString(),
        duration: duration,        // 专注时长（秒）
        goal: goal,                // 目标时长（分钟）
        completed: duration >= goal * 60
    });
    
    saveRecords(records);
    return records;
}

/**
 * 清除所有记录
 */
function clearRecords() {
    saveRecords([]);
}

// ==================== 时间格式化 ====================

/**
 * 秒数转换为时分秒格式
 */
function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
        return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

/**
 * 秒数转换为小时:分钟格式
 */
function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    
    if (hours > 0) {
        return `${hours}小时${minutes}分钟`;
    }
    return `${minutes}分钟`;
}

/**
 * 获取今天的日期字符串
 */
function getTodayString() {
    const now = new Date();
    return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
}

/**
 * 获取本周的日期范围
 */
function getWeekRange() {
    const now = new Date();
    const dayOfWeek = now.getDay();
    const startOfWeek = new Date(now);
    startOfWeek.setDate(now.getDate() - dayOfWeek);
    
    const dates = [];
    for (let i = 0; i < 7; i++) {
        const date = new Date(startOfWeek);
        date.setDate(startOfWeek.getDate() + i);
        dates.push(date);
    }
    return dates;
}

// ==================== 统计数据 ====================

/**
 * 计算今日专注时长
 */
function getTodayFocusTime() {
    const records = getRecords();
    const today = getTodayString();
    
    return records
        .filter(r => r.date.startsWith(today))
        .reduce((sum, r) => sum + r.duration, 0);
}

/**
 * 计算本周专注时长
 */
function getWeekFocusTime() {
    const records = getRecords();
    const weekDates = getWeekRange();
    const today = getTodayString();
    
    return records
        .filter(r => {
            const recordDate = r.date.split('T')[0];
            return weekDates.some(d => {
                const dStr = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
                return recordDate === dStr;
            });
        })
        .reduce((sum, r) => sum + r.duration, 0);
}

/**
 * 获取今日专注次数
 */
function getTodaySessionCount() {
    const records = getRecords();
    const today = getTodayString();
    
    return records.filter(r => r.date.startsWith(today)).length;
}

/**
 * 获取本周每天的专注时长
 */
function getWeekDailyTime() {
    const weekDates = getWeekRange();
    const records = getRecords();
    
    return weekDates.map(date => {
        const dateStr = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
        const total = records
            .filter(r => r.date.startsWith(dateStr))
            .reduce((sum, r) => sum + r.duration, 0);
        return { date, total };
    });
}

// ==================== UI 更新 ====================

/**
 * 更新统计数据
 */
function updateStats() {
    const todaySec = getTodayFocusTime();
    const weekSec = getWeekFocusTime();
    const sessions = getTodaySessionCount();
    
    todayTime.textContent = formatDuration(todaySec);
    weekTime.textContent = formatDuration(weekSec);
    sessionCount.textContent = sessions;
    
    // 更新本周图表
    updateWeekChart();
    
    // 更新历史记录
    updateHistory();
}

/**
 * 更新本周趋势图
 */
function updateWeekChart() {
    const weekData = getWeekDailyTime();
    const today = getTodayString();
    const maxTime = Math.max(...weekData.map(d => d.total), 3600); // 最小1小时作为最大值
    
    // 生成柱状图
    weekChart.innerHTML = weekData.map(d => {
        const dateStr = `${d.date.getFullYear()}-${String(d.date.getMonth() + 1).padStart(2, '0')}-${String(d.date.getDate()).padStart(2, '0')}`;
        const isToday = dateStr === today;
        const height = d.total > 0 ? Math.max((d.total / maxTime) * 80, 4) : 4;
        
        return `
            <div class="chart-bar ${isToday ? 'today' : ''}" 
                 style="height: ${height}px;"
                 title="${formatDuration(d.total)}">
                <span class="bar-value">${d.total > 0 ? formatDuration(d.total) : ''}</span>
            </div>
        `;
    }).join('');
    
    // 生成标签
    chartLabels.innerHTML = weekData.map(d => {
        const isToday = d.date.toDateString() === new Date().toDateString();
        return `<span class="chart-label ${isToday ? 'today' : ''}">${WEEKDAYS[d.date.getDay()]}</span>`;
    }).join('');
}

/**
 * 更新历史记录列表
 */
function updateHistory() {
    const records = getRecords();
    const recentRecords = records.slice(-5).reverse();
    
    if (recentRecords.length === 0) {
        historyList.innerHTML = '<div class="history-empty">暂无专注记录，开始你的第一次专注吧！</div>';
        return;
    }
    
    historyList.innerHTML = recentRecords.map(r => {
        const date = new Date(r.date);
        const dateStr = `${date.getMonth() + 1}/${date.getDate()} ${WEEKDAYS[date.getDay()]} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
        return `
            <div class="history-item">
                <span class="history-date">${dateStr}</span>
                <span class="history-duration">${formatDuration(r.duration)}</span>
            </div>
        `;
    }).join('');
}

// ==================== 计时器控制 ====================

/**
 * 开始专注
 */
function startFocus() {
    isFocusing = true;
    focusStartTime = Date.now();
    elapsedSeconds = 0;
    distractionCount = 0;
    
    // 更新UI
    timerDisplay.textContent = formatTime(0);
    statusBadge.className = 'status-badge focusing';
    statusText.textContent = '专注中';
    controlBtn.className = 'control-btn end';
    controlBtn.innerHTML = '<span>⏹</span> 结束专注';
    
    // 开始计时
    timerInterval = setInterval(() => {
        elapsedSeconds = Math.floor((Date.now() - focusStartTime) / 1000);
        timerDisplay.textContent = formatTime(elapsedSeconds);
        
        // 检测分心（页面隐藏）
        if (document.hidden) {
            handleDistraction();
        }
    }, 1000);
    
    showToast('专注开始！保持专注，相信你能行 💪', 'success');
}

/**
 * 结束专注
 */
function endFocus(save = true) {
    if (!isFocusing) return;
    
    isFocusing = false;
    
    // 停止计时
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
    
    // 保存记录
    if (save && elapsedSeconds >= 60) { // 至少专注1分钟才保存
        addRecord(elapsedSeconds, currentGoal);
        showToast(`太棒了！本次专注 ${formatTime(elapsedSeconds)}`, 'success');
    }
    
    // 重置UI
    timerDisplay.textContent = formatTime(0);
    statusBadge.className = 'status-badge idle';
    statusText.textContent = '等待开始';
    controlBtn.className = 'control-btn start';
    controlBtn.innerHTML = '<span>▶</span> 开始专注';
    
    // 更新统计
    updateStats();
}

/**
 * 处理分心事件（切换标签页/最小化）
 */
function handleDistraction() {
    distractionCount++;
    warningCount.textContent = distractionCount;
    focusWarning.classList.add('show');
}

/**
 * 继续专注
 */
function continueFocus() {
    focusWarning.classList.remove('show');
    // 继续计时，不中断
}

/**
 * 放弃专注
 */
function giveUpFocus() {
    focusWarning.classList.remove('show');
    endFocus(true); // 保存本次记录
}

// ==================== Toast 提示 ====================

/**
 * 显示 Toast 提示
 */
function showToast(message, type = 'success') {
    toastIcon.textContent = type === 'success' ? '✓' : '⚠';
    toastMessage.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ==================== 事件绑定 ====================

// 目标时长选择
goalBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        if (isFocusing) return; // 专注中不能切换目标
        
        goalBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentGoal = parseInt(btn.dataset.goal);
    });
});

// 控制按钮
controlBtn.addEventListener('click', () => {
    if (isFocusing) {
        endFocus(true);
    } else {
        startFocus();
    }
});

// 继续专注按钮
continueBtn.addEventListener('click', continueFocus);

// 放弃按钮
giveUpBtn.addEventListener('click', giveUpFocus);

// 清除记录按钮
clearBtn.addEventListener('click', () => {
    if (confirm('确定要清除所有专注记录吗？此操作不可恢复。')) {
        clearRecords();
        updateStats();
        showToast('记录已清除', 'warning');
    }
});

// 页面可见性变化（检测切换标签）
document.addEventListener('visibilitychange', () => {
    if (isFocusing && document.hidden) {
        handleDistraction();
    }
});

// 页面卸载提示
window.addEventListener('beforeunload', (e) => {
    if (isFocusing) {
        e.preventDefault();
        e.returnValue = '专注尚未结束，确定要离开吗？';
    }
});

// 键盘快捷键
document.addEventListener('keydown', (e) => {
    // 空格键开始/结束专注
    if (e.code === 'Space' && e.target.tagName !== 'BUTTON') {
        e.preventDefault();
        if (isFocusing) {
            endFocus(true);
        } else {
            startFocus();
        }
    }
});

// ==================== 初始化 ====================

/**
 * 初始化应用
 */
function init() {
    // 设置默认目标
    const defaultBtn = document.querySelector('.goal-btn[data-goal="25"]');
    if (defaultBtn) defaultBtn.classList.add('active');
    
    // 恢复未完成的专注（页面刷新后）
    // 这里简单处理，实际可以结合会话存储
    const unfinishedFocus = sessionStorage.getItem('unfinished_focus');
    if (unfinishedFocus) {
        try {
            const data = JSON.parse(unfinishedFocus);
            if (data.startTime) {
                // 计算经过的时间
                const elapsed = Math.floor((Date.now() - data.startTime) / 1000);
                if (elapsed < currentGoal * 60 * 2) { // 超过目标2倍则忽略
                    elapsedSeconds = elapsed;
                    focusStartTime = data.startTime;
                    isFocusing = true;
                    
                    timerDisplay.textContent = formatTime(elapsedSeconds);
                    statusBadge.className = 'status-badge focusing';
                    statusText.textContent = '专注中';
                    controlBtn.className = 'control-btn end';
                    controlBtn.innerHTML = '<span>⏹</span> 结束专注';
                    
                    timerInterval = setInterval(() => {
                        elapsedSeconds = Math.floor((Date.now() - focusStartTime) / 1000);
                        timerDisplay.textContent = formatTime(elapsedSeconds);
                        
                        if (document.hidden) {
                            handleDistraction();
                        }
                    }, 1000);
                    
                    showToast('检测到未完成的专注，继续计时中...', 'warning');
                }
            }
        } catch (e) {
            console.error('恢复专注失败:', e);
        }
        sessionStorage.removeItem('unfinished_focus');
    }
    
    // 更新统计数据
    updateStats();
    
    console.log('🎯 专注时长统计 - 初始化完成');
    console.log('💡 快捷键: 空格键 开始/结束专注');
}

// 启动应用
init();
