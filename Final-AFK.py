import pyautogui
import time
import keyboard


# ================= 核心配置参数 =================
STOP_KEY = 'p'
BATTLE_DURATION = 62  # 战斗时长（秒）

# 1. 道具结算参数 (keyboard 库驱动)
SETTLE_COUNT = 200  # 结算循环次数
F_HOLD_TIME = 0.1  # 按下 F 的持续时间
F_INTERVAL = 0.1      # 按键间隔

# 2. 升级阶段参数
UPGRADE_FLAG_IMG = 'upgrade_flag.png'
UPGRADE_ATTR_POS = (525, 1300)
UPGRADE_FLAG_REGION = (1361, 525, 300, 150)
UPGRADE_CONFIDENCE = 0.7

# 3. 商店阶段参数
TARGET_IMAGE = 'target_item.png'
SHOP_CONFIDENCE = 0.4
SHOP_BUY_POS = [(495, 1146), (1122, 1146), (1828, 1146), (2521, 1146)]
SHOP_REGIONS = [
    (167, 339, 200, 200), (852, 339, 200, 200),
    (1547, 339, 200, 200), (2234, 339, 200, 200)
]
SHOP_REFRESH_POS = (2557, 167)
SHOP_CONTINUE_FIGHT_POS = (3206, 1971)

# 4. 锁定检测参数
LOCK_IMG = 'Lock.png'
LOCK_REGION = (642, 1250, 109, 84)
LOCK_CLICK_POS = (642, 1250)
LOCK_CONFIDENCE = 0.4


# ================= 阶段功能函数 =================

def run_settlement_phase():
    """阶段 2: 道具结算"""
    print("📦 正在结算道具 (keyboard 驱动)...")
    time.sleep(2)  # 等待结算界面弹出动画
    for i in range(SETTLE_COUNT):
        if keyboard.is_pressed(STOP_KEY): return False

        keyboard.press('f')
        time.sleep(F_HOLD_TIME)
        keyboard.release('f')
        time.sleep(F_INTERVAL)

        if (i + 1) % 50 == 0:
            print(f"  -> 已尝试按 F 共 {i + 1} 次...")
    return True


def run_upgrade_phase():
    """阶段 3: 动态属性升级"""
    print("\n🆙 开始属性升级阶段...")
    # 初始 100 次快速点击
    for i in range(100):
        if keyboard.is_pressed(STOP_KEY): return False
        pyautogui.click(UPGRADE_ATTR_POS)
        time.sleep(0.05)

    cycle = 1
    while True:
        if keyboard.is_pressed(STOP_KEY): return False
        try:
            res = pyautogui.locateOnScreen(
                UPGRADE_FLAG_IMG,
                region=UPGRADE_FLAG_REGION,
                confidence=UPGRADE_CONFIDENCE
            )
            if res:
                print(f"  -> 仍在升级界面，追加点击第 {cycle} 组 (20次)...")
                for _ in range(20):
                    pyautogui.click(UPGRADE_ATTR_POS)
                    time.sleep(0.05)
                cycle += 1
            else:
                break
        except:
            break
    print("🏁 升级阶段完成")
    time.sleep(1.5)
    return True


def check_and_unlock():
    """检查并解除锁定"""
    print("\n🔒 检查锁定状态...")
    try:
        # 在指定区域查找锁定图标
        lock_res = pyautogui.locateOnScreen(
            LOCK_IMG,
            region=LOCK_REGION,
            confidence=LOCK_CONFIDENCE
        )
        if lock_res:
            print("🔐 检测到锁定，正在解除...")
            pyautogui.click(LOCK_CLICK_POS)
            time.sleep(0.5)  # 等待解锁动画
            return True
        else:
            print("✅ 未检测到锁定，继续执行...")
            return False
    except:
        print("✅ 未检测到锁定，继续执行...")
        return False


def run_shop_phase():
    """阶段 4: 商店选购逻辑"""
    print("\n🛒 商店扫描启动...")
    refresh_count = 0
    while True:
        if keyboard.is_pressed(STOP_KEY): return False

        found_item = False
        for i in range(4):
            try:
                res = pyautogui.locateOnScreen(
                    TARGET_IMAGE,
                    region=SHOP_REGIONS[i],
                    confidence=SHOP_CONFIDENCE
                )
                if res:
                    print(f"💰 在位置 {i + 1} 找到目标！执行购买...")
                    pyautogui.click(SHOP_BUY_POS[i])
                    time.sleep(0.5)
                    found_item = True
                    break
            except:
                continue

        if found_item:
            print("✅ 购买成功，准备下一波战斗")
            pyautogui.click(SHOP_CONTINUE_FIGHT_POS)
            time.sleep(2)
            return True
        else:
            print(f"♻️ 未发现目标，执行第 {refresh_count + 1} 次刷新...")
            pyautogui.click(SHOP_REFRESH_POS)
            refresh_count += 1
            time.sleep(1.5)


# ================= 主程序入口 =================

def main():
    print("=== Brotato 全自动挂机脚本运行中 ===")
    print(f"停止键: 长按 '{STOP_KEY.upper()}' | 模式: keyboard + pyautogui 混合驱动")
    print("请在 5 秒内切换至游戏界面...")
    time.sleep(5)

    wave = 1
    while True:
        if keyboard.is_pressed(STOP_KEY):
            print("🛑 脚本已停止")
            break

        # 1. 战斗阶段
        print(f"\n⚔️ [第 {wave} 波] 战斗挂机中 ({BATTLE_DURATION}s)...")
        time.sleep(BATTLE_DURATION)

        # 2. 结算阶段
        if not run_settlement_phase(): break

        # 3. 升级阶段
        if not run_upgrade_phase(): break

        # 新增：检查并解除锁定
        check_and_unlock()

        # 4. 商店阶段
        if not run_shop_phase(): break

        print(f"\n✨ 第 {wave} 波流程处理完毕")
        wave += 1


if __name__ == "__main__":
    try:
        # 注意：使用 keyboard 库和操作某些游戏窗口时，请务必以"管理员身份"运行编辑器
        main()
    except Exception as e:
        print(f"❌ 运行报错: {e}")
    finally:
        print("脚本已安全退出。")