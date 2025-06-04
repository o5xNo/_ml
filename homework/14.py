import gymnasium as gym
import time

env = gym.make("CartPole-v1", render_mode="human")

total_steps = 0

for episode in range(10):  # 執行 10 回合
    observation, info = env.reset(seed=episode)  # 每回合用不同 seed
    steps = 0
    done = False

    while not done:
        env.render()
        time.sleep(0.01)  # 每 0.01 秒更新一次畫面

        # 固定策略：根據 pole angle 來控制方向
        angle = observation[2]
        action = 1 if angle > 0 else 0

        observation, reward, terminated, truncated, info = env.step(action)
        steps += 1

        if terminated or truncated:
            print(f'Episode {episode + 1} 結束，撐了 {steps} 步')
            total_steps += steps
            break

env.close()
print(f'🏁 共 10 回合，總共撐了 {total_steps} 步')
