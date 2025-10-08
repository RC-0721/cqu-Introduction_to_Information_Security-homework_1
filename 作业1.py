import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time


class SDES:
    def __init__(self):
        # 定义所有置换盒
        self.P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
        self.P8 = [6, 3, 7, 4, 8, 5, 10, 9]
        self.IP = [2, 6, 3, 1, 4, 8, 5, 7]
        self.IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]
        self.EP = [4, 1, 2, 3, 2, 3, 4, 1]
        self.P4 = [2, 4, 3, 1]

        # S盒
        self.S0 = [
            [1, 0, 3, 2],
            [3, 2, 1, 0],
            [0, 2, 1, 3],
            [3, 1, 0, 2]
        ]

        self.S1 = [
            [0, 1, 2, 3],
            [2, 3, 1, 0],
            [3, 0, 1, 2],
            [2, 1, 0, 3]
        ]

    def permute(self, bits, permutation):
        """执行置换操作"""
        return ''.join(bits[i - 1] for i in permutation)

    def left_shift(self, bits, n):
        """循环左移"""
        return bits[n:] + bits[:n]

    def generate_keys(self, key):
        """生成子密钥K1和K2"""
        # P10置换
        p10_key = self.permute(key, self.P10)

        # 分成左右两部分
        left = p10_key[:5]
        right = p10_key[5:]

        # 生成K1：左移1位后P8置换
        left_shift1_left = self.left_shift(left, 1)
        left_shift1_right = self.left_shift(right, 1)
        k1 = self.permute(left_shift1_left + left_shift1_right, self.P8)

        # 生成K2：左移2位后P8置换
        left_shift2_left = self.left_shift(left_shift1_left, 2)
        left_shift2_right = self.left_shift(left_shift1_right, 2)
        k2 = self.permute(left_shift2_left + left_shift2_right, self.P8)

        return k1, k2

    def f_function(self, right, subkey):
        """轮函数f"""
        # 扩展置换
        expanded = self.permute(right, self.EP)

        # 与子密钥异或
        xor_result = ''.join(str(int(expanded[i]) ^ int(subkey[i])) for i in range(8))

        # S盒替换
        left_sbox = xor_result[:4]
        right_sbox = xor_result[4:]

        # S0盒
        s0_row = int(left_sbox[0] + left_sbox[3], 2)
        s0_col = int(left_sbox[1] + left_sbox[2], 2)
        s0_output = format(self.S0[s0_row][s0_col], '02b')

        # S1盒
        s1_row = int(right_sbox[0] + right_sbox[3], 2)
        s1_col = int(right_sbox[1] + right_sbox[2], 2)
        s1_output = format(self.S1[s1_row][s1_col], '02b')

        # P4置换
        s_output = s0_output + s1_output
        return self.permute(s_output, self.P4)

    def encrypt_block(self, plaintext, key):
        """加密一个8位分组"""
        k1, k2 = self.generate_keys(key)

        # 初始置换
        ip_result = self.permute(plaintext, self.IP)

        # 第一轮
        left1 = ip_result[:4]
        right1 = ip_result[4:]
        f_result1 = self.f_function(right1, k1)
        new_right1 = ''.join(str(int(left1[i]) ^ int(f_result1[i])) for i in range(4))

        # 交换
        left2 = right1
        right2 = new_right1

        # 第二轮
        f_result2 = self.f_function(right2, k2)
        new_right2 = ''.join(str(int(left2[i]) ^ int(f_result2[i])) for i in range(4))

        # 最终置换
        final_result = new_right2 + right2
        return self.permute(final_result, self.IP_inv)

    def decrypt_block(self, ciphertext, key):
        """解密一个8位分组"""
        k1, k2 = self.generate_keys(key)

        # 初始置换
        ip_result = self.permute(ciphertext, self.IP)

        # 第一轮（使用K2）
        left1 = ip_result[:4]
        right1 = ip_result[4:]
        f_result1 = self.f_function(right1, k2)
        new_right1 = ''.join(str(int(left1[i]) ^ int(f_result1[i])) for i in range(4))

        # 交换
        left2 = right1
        right2 = new_right1

        # 第二轮（使用K1）
        f_result2 = self.f_function(right2, k1)
        new_right2 = ''.join(str(int(left2[i]) ^ int(f_result2[i])) for i in range(4))

        # 最终置换
        final_result = new_right2 + right2
        return self.permute(final_result, self.IP_inv)

    def text_to_binary(self, text):
        """将文本转换为二进制字符串"""
        binary_str = ''
        for char in text:
            binary_str += format(ord(char), '08b')
        return binary_str

    def binary_to_text(self, binary_str):
        """将二进制字符串转换为文本"""
        text = ''
        for i in range(0, len(binary_str), 8):
            byte = binary_str[i:i + 8]
            if len(byte) == 8:
                text += chr(int(byte, 2))
        return text

    def encrypt_text(self, plaintext, key):
        """加密文本"""
        binary_text = self.text_to_binary(plaintext)
        encrypted_binary = ''

        for i in range(0, len(binary_text), 8):
            block = binary_text[i:i + 8]
            if len(block) == 8:
                encrypted_block = self.encrypt_block(block, key)
                encrypted_binary += encrypted_block

        return self.binary_to_text(encrypted_binary)

    def decrypt_text(self, ciphertext, key):
        """解密文本"""
        binary_text = self.text_to_binary(ciphertext)
        decrypted_binary = ''

        for i in range(0, len(binary_text), 8):
            block = binary_text[i:i + 8]
            if len(block) == 8:
                decrypted_block = self.decrypt_block(block, key)
                decrypted_binary += decrypted_block

        return self.binary_to_text(decrypted_binary)

    def brute_force_attack(self, plaintext, ciphertext, progress_callback=None):
        """暴力破解密钥"""
        start_time = time.time()
        found_keys = []

        # 遍历所有可能的10位密钥
        for i in range(1024):
            key = format(i, '010b')

            # 更新进度
            if progress_callback and i % 100 == 0:
                progress_callback(i / 1024 * 100)

            try:
                encrypted = self.encrypt_block(plaintext, key)
                if encrypted == ciphertext:
                    found_keys.append(key)
            except:
                continue

        end_time = time.time()
        return found_keys, end_time - start_time


class SDESGUI:
    def __init__(self):
        self.sdes = SDES()
        self.root = tk.Tk()
        self.root.title("S-DES算法实现")
        self.root.geometry("800x600")

        self.setup_gui()

        # 暴力破解线程控制
        self.brute_force_running = False

    def setup_gui(self):
        # 创建标签页
        notebook = ttk.Notebook(self.root)

        # 基本加解密标签页
        basic_frame = ttk.Frame(notebook)
        self.setup_basic_tab(basic_frame)

        # 文本加解密标签页
        text_frame = ttk.Frame(notebook)
        self.setup_text_tab(text_frame)

        # 暴力破解标签页
        brute_frame = ttk.Frame(notebook)
        self.setup_brute_force_tab(brute_frame)

        # 分析标签页
        analysis_frame = ttk.Frame(notebook)
        self.setup_analysis_tab(analysis_frame)

        notebook.add(basic_frame, text="基本加解密")
        notebook.add(text_frame, text="文本加解密")
        notebook.add(brute_frame, text="暴力破解")
        notebook.add(analysis_frame, text="封闭测试")
        notebook.pack(expand=True, fill='both', padx=10, pady=10)

    def setup_basic_tab(self, parent):
        # 明文输入
        ttk.Label(parent, text="明文 (8位二进制):").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.plaintext_entry = ttk.Entry(parent, width=20)
        self.plaintext_entry.grid(row=0, column=1, padx=5, pady=5)

        # 密钥输入
        ttk.Label(parent, text="密钥 (10位二进制):").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.key_entry = ttk.Entry(parent, width=20)
        self.key_entry.grid(row=1, column=1, padx=5, pady=5)

        # 加密按钮
        encrypt_btn = ttk.Button(parent, text="加密", command=self.encrypt_basic)
        encrypt_btn.grid(row=2, column=0, padx=5, pady=10)

        # 解密按钮
        decrypt_btn = ttk.Button(parent, text="解密", command=self.decrypt_basic)
        decrypt_btn.grid(row=2, column=1, padx=5, pady=10)

        # 结果显示
        ttk.Label(parent, text="结果:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.result_text = scrolledtext.ScrolledText(parent, width=50, height=10)
        self.result_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def setup_text_tab(self, parent):
        # 文本输入
        ttk.Label(parent, text="文本:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.text_input = scrolledtext.ScrolledText(parent, width=50, height=5)
        self.text_input.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # 密钥输入
        ttk.Label(parent, text="密钥 (10位二进制):").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.text_key_entry = ttk.Entry(parent, width=20)
        self.text_key_entry.grid(row=2, column=1, padx=5, pady=5)

        # 按钮框架
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        encrypt_text_btn = ttk.Button(btn_frame, text="加密文本", command=self.encrypt_text)
        encrypt_text_btn.pack(side='left', padx=5)

        decrypt_text_btn = ttk.Button(btn_frame, text="解密文本", command=self.decrypt_text)
        decrypt_text_btn.pack(side='left', padx=5)

        # 结果显示
        ttk.Label(parent, text="结果:").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        self.text_result = scrolledtext.ScrolledText(parent, width=50, height=10)
        self.text_result.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def setup_brute_force_tab(self, parent):
        # 已知明密文对
        ttk.Label(parent, text="已知明文 (8位二进制):").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.known_plaintext = ttk.Entry(parent, width=20)
        self.known_plaintext.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(parent, text="已知密文 (8位二进制):").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.known_ciphertext = ttk.Entry(parent, width=20)
        self.known_ciphertext.grid(row=1, column=1, padx=5, pady=5)

        # 进度条
        ttk.Label(parent, text="破解进度:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(parent, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=2, column=1, sticky='ew', padx=5, pady=5)

        # 暴力破解按钮
        brute_btn = ttk.Button(parent, text="开始暴力破解", command=self.start_brute_force)
        brute_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # 结果显示
        ttk.Label(parent, text="破解结果:").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        self.brute_force_result = scrolledtext.ScrolledText(parent, width=50, height=10)
        self.brute_force_result.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def setup_analysis_tab(self, parent):
        ttk.Label(parent, text="封闭测试分析", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky='w', pady=10)

        analysis_text = """
S-DES算法封闭测试分析：

1. 密钥空间分析：
   - 密钥长度：10位
   - 密钥空间大小：2^10 = 1024种可能密钥

2. 多密钥情况分析：
   - 对于给定的明密文对，可能存在多个密钥能够产生相同的加密结果
   - 这是由于S-DES的简化结构导致的碰撞

3. 安全性分析：
   - 由于密钥空间较小，S-DES容易受到暴力破解攻击
   - 实际DES使用56位密钥，密钥空间大得多

4. 碰撞分析：
   - 对于不同的密钥 Ki ≠ Kj，可能加密得到相同的密文
   - 这是由于密码算法的非线性特性导致的
        """

        analysis_display = scrolledtext.ScrolledText(parent, width=70, height=20)
        analysis_display.grid(row=1, column=0, padx=10, pady=10)
        analysis_display.insert('1.0', analysis_text)
        analysis_display.config(state='disabled')

    def encrypt_basic(self):
        try:
            plaintext = self.plaintext_entry.get().strip()
            key = self.key_entry.get().strip()

            if len(plaintext) != 8 or not all(c in '01' for c in plaintext):
                messagebox.showerror("错误", "明文必须是8位二进制数")
                return

            if len(key) != 10 or not all(c in '01' for c in key):
                messagebox.showerror("错误", "密钥必须是10位二进制数")
                return

            ciphertext = self.sdes.encrypt_block(plaintext, key)

            result = f"明文: {plaintext}\n"
            result += f"密钥: {key}\n"
            result += f"密文: {ciphertext}\n"
            result += f"K1: {self.sdes.generate_keys(key)[0]}\n"
            result += f"K2: {self.sdes.generate_keys(key)[1]}"

            self.result_text.delete('1.0', tk.END)
            self.result_text.insert('1.0', result)

        except Exception as e:
            messagebox.showerror("错误", f"加密失败: {str(e)}")

    def decrypt_basic(self):
        try:
            ciphertext = self.plaintext_entry.get().strip()
            key = self.key_entry.get().strip()

            if len(ciphertext) != 8 or not all(c in '01' for c in ciphertext):
                messagebox.showerror("错误", "密文必须是8位二进制数")
                return

            if len(key) != 10 or not all(c in '01' for c in key):
                messagebox.showerror("错误", "密钥必须是10位二进制数")
                return

            plaintext = self.sdes.decrypt_block(ciphertext, key)

            result = f"密文: {ciphertext}\n"
            result += f"密钥: {key}\n"
            result += f"明文: {plaintext}\n"
            result += f"K1: {self.sdes.generate_keys(key)[0]}\n"
            result += f"K2: {self.sdes.generate_keys(key)[1]}"

            self.result_text.delete('1.0', tk.END)
            self.result_text.insert('1.0', result)

        except Exception as e:
            messagebox.showerror("错误", f"解密失败: {str(e)}")

    def encrypt_text(self):
        try:
            text = self.text_input.get('1.0', tk.END).strip()
            key = self.text_key_entry.get().strip()

            if len(key) != 10 or not all(c in '01' for c in key):
                messagebox.showerror("错误", "密钥必须是10位二进制数")
                return

            encrypted_text = self.sdes.encrypt_text(text, key)

            result = f"原始文本: {text}\n"
            result += f"密钥: {key}\n"
            result += f"加密结果: {encrypted_text}\n"
            result += f"十六进制: {encrypted_text.encode('latin-1').hex()}"

            self.text_result.delete('1.0', tk.END)
            self.text_result.insert('1.0', result)

        except Exception as e:
            messagebox.showerror("错误", f"文本加密失败: {str(e)}")

    def decrypt_text(self):
        try:
            text = self.text_input.get('1.0', tk.END).strip()
            key = self.text_key_entry.get().strip()

            if len(key) != 10 or not all(c in '01' for c in key):
                messagebox.showerror("错误", "密钥必须是10位二进制数")
                return

            decrypted_text = self.sdes.decrypt_text(text, key)

            result = f"加密文本: {text}\n"
            result += f"密钥: {key}\n"
            result += f"解密结果: {decrypted_text}"

            self.text_result.delete('1.0', tk.END)
            self.text_result.insert('1.0', result)

        except Exception as e:
            messagebox.showerror("错误", f"文本解密失败: {str(e)}")

    def update_progress(self, value):
        self.progress_var.set(value)
        self.root.update_idletasks()

    def brute_force_thread(self):
        plaintext = self.known_plaintext.get().strip()
        ciphertext = self.known_ciphertext.get().strip()

        if len(plaintext) != 8 or not all(c in '01' for c in plaintext):
            self.brute_force_result.insert(tk.END, "错误: 明文必须是8位二进制数\n")
            return

        if len(ciphertext) != 8 or not all(c in '01' for c in ciphertext):
            self.brute_force_result.insert(tk.END, "错误: 密文必须是8位二进制数\n")
            return

        found_keys, time_taken = self.sdes.brute_force_attack(
            plaintext, ciphertext, self.update_progress
        )

        result = f"暴力破解完成！耗时: {time_taken:.4f}秒\n"
        result += f"测试密钥数: 1024\n"

        if found_keys:
            result += f"找到 {len(found_keys)} 个可能的密钥:\n"
            for key in found_keys:
                result += f"密钥: {key} (十进制: {int(key, 2)})\n"
        else:
            result += "未找到匹配的密钥\n"

        self.brute_force_result.delete('1.0', tk.END)
        self.brute_force_result.insert('1.0', result)
        self.brute_force_running = False

    def start_brute_force(self):
        if self.brute_force_running:
            return

        self.brute_force_running = True
        self.brute_force_result.delete('1.0', tk.END)
        self.brute_force_result.insert(tk.END, "开始暴力破解...\n")

        thread = threading.Thread(target=self.brute_force_thread)
        thread.daemon = True
        thread.start()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    # 测试示例
    app = SDESGUI()
    app.run()
