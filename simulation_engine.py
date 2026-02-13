import random
import time
import sys
from colorama import init, Fore, Back, Style

# Initialize Colorama
init(autoreset=True)

class SimulationEngine:
    def __init__(self, detector, X_test, y_test):
        self.detector = detector
        self.X_test = X_test
        self.y_test = y_test
        self.stats = {"processed": 0, "blocked": 0, "safe": 0}
        self.results = []

    def generate_fake_ip(self):
        return f"{random.randint(10, 192)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

    def print_header(self):
        print("\n" + "="*80)
        print(f"{Fore.CYAN}{Style.BRIGHT}{'ADAPTIVE ZERO-DAY THREAT IDENTIFICATION SYSTEM':^80}{Style.RESET_ALL}")
        print("="*80)
        # Manual table header
        print(f"{Fore.WHITE}{Style.BRIGHT}| {'TIMESTAMP':<12} | {'SOURCE IP':<15} | {'PROTOCOL':<8} | {'STATUS':<10} | {'ACTION':<15} |{Style.RESET_ALL}")
        print("-" * 80)

    def run(self, num_packets=20):
        self.print_header()
        
        for i in range(num_packets):
            # Simulate packet
            if i >= len(self.X_test): break
            packet = self.X_test.iloc[i].values
            actual_label = self.y_test.iloc[i]
            
            # Fake metadata
            timestamp = time.strftime("%H:%M:%S")
            src_ip = self.generate_fake_ip()
            protocol = "TCP" if random.random() > 0.3 else "UDP"
            
            # 1. Proxy Layer (Trusted Bypass)
            is_trusted = random.random() < 0.1 # 10% chance
            
            if is_trusted:
                status = "TRUSTED"
                action = "BYPASS"
                color = Fore.GREEN
                self.stats["safe"] += 1
                self.results.append((actual_label, 0))
            else:
                # 2. Sandbox Quarantine
                # print(f"{Fore.YELLOW}Scanning...{Style.RESET_ALL}", end="\r")
                # time.sleep(0.2) # Delay for realism
                
                score, is_threat = self.detector.predict(packet)
                
                if is_threat:
                    status = "THREAT"
                    action = "QUARANTINE"
                    color = Back.RED + Fore.WHITE
                    self.stats["blocked"] += 1
                    self.results.append((actual_label, 1))
                    
                    # Print the row first
                    row = f"| {timestamp:<12} | {src_ip:<15} | {protocol:<8} | {color}{status:<10}{Style.RESET_ALL} | {color}{action:<15}{Style.RESET_ALL} |"
                    print(row)
                    
                    # 3. HITL (Admin Verification)
                    self.handle_threat(packet)
                    continue # Skip printing the row again
                    
                else:
                    status = "SAFE"
                    action = "ALLOWED"
                    color = Fore.GREEN
                    self.stats["safe"] += 1
                    self.results.append((actual_label, 0))

            # Print row
            row = f"| {timestamp:<12} | {src_ip:<15} | {protocol:<8} | {color}{status:<10}{Style.RESET_ALL} | {color}{action:<15}{Style.RESET_ALL} |"
            print(row)
            time.sleep(0.3) # Delay between packets

        print("-" * 80)
        print(f"\n{Fore.CYAN}[*] Simulation Complete.{Style.RESET_ALL}")
        return self.stats, self.results

    def handle_threat(self, packet):
        print(f"\n{Fore.RED}{Style.BRIGHT}    [!] ALERT: Zero-Day Anomaly Detected! Requesting Admin Action...{Style.RESET_ALL}")
        time.sleep(1)
        print(f"{Fore.YELLOW}    > Admin Console: Verifying Packet Signature...{Style.RESET_ALL}")
        time.sleep(1)
        
        # Simulate Admin Choice (Randomly Release or Block for the demo)
        # In a real demo, we might ask input, but for "Hollywood" flow, auto-action is smoother unless specified.
        # User asked: "Simulate the Admin confirming the block"
        
        print(f"{Fore.RED}    > ADMIN DECISION: BLOCKED PERMANENTLY.{Style.RESET_ALL}")
        print(f"{Fore.GREEN}    > Feedback Loop: Model Updated.{Style.RESET_ALL}\n")
        time.sleep(1)
