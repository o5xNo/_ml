import gymnasium as gym
import time

env = gym.make("CartPole-v1", render_mode="human")

total_steps = 0

for episode in range(10):
    observation, info = env.reset(seed=episode)
    steps = 0
    done = False

    while not done:
        env.render()
        time.sleep(0.0001)

        angle = observation[2] #位置、速度、擺錘的角度、角速度
        
        if angle > 0: # 根據角度決定動作：如果角度大於0，動作為1(推向右邊)，否則為0(推向左邊)。向右:負角度 向左:正角度
            action = 1
        else:
            action = 0 
        '''
        angle = observation[2]
        angular_velocity = observation[3]

        # 根據角度 + 角速度決定動作
        if angle + angular_velocity > 0:
            action = 1
        else:
            action = 0
        '''

        observation, reward, terminated, truncated, info = env.step(action) #terminated：布林值，表示是否達到終止條件（比如遊戲輸贏、失敗等）。truncated：布林值，表示是否因為時間限制或其他外部條件而提前結束。
        steps += 1

        if terminated or truncated:
            print(f'Episode {episode + 1} 結束，撐了 {steps} 步')
            total_steps += steps
            break

env.close()
print(f'🏁 共 10 回合，總共撐了 {total_steps} 步')
