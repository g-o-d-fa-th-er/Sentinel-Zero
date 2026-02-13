import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import sys
import os

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

from data_loader import get_data
from ensemble_model import ThreatDetector
from simulation_engine import SimulationEngine
from colorama import Fore, Style

def plot_stats(stats):
    """Generates a bar chart of the simulation stats."""
    print(f"\n{Fore.CYAN}[*] Generating Traffic Statistics Chart...{Style.RESET_ALL}")
    
    categories = ['Safe', 'Blocked']
    values = [stats['safe'], stats['blocked']]
    
    plt.figure(figsize=(8, 6))
    sns.barplot(x=categories, y=values, palette=['green', 'red'])
    plt.title('Simulation Results: Normal vs Blocked Traffic')
    plt.ylabel('Packet Count')
    
    # Save
    plt.savefig('traffic_stats.png')
    print(f"{Fore.GREEN}[+] Chart saved as 'traffic_stats.png'.{Style.RESET_ALL}")

def main():
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{Fore.CYAN}[*] Initializing System...{Style.RESET_ALL}")
    
    # 1. Load Data
    try:
        X_train, X_test, y_train, y_test = get_data()
    except Exception as e:
        print(f"{Fore.RED}[!] Data Loading Failed: {e}{Style.RESET_ALL}")
        return

    # 2. Train Model
    detector = ThreatDetector()
    detector.train(X_train)
    
    # 3. Start Simulation
    sim = SimulationEngine(detector, X_test, y_test)
    
    # Ask for packet count (optional, default 20 for demo)
    try:
        num = input(f"\n{Fore.YELLOW}Enter number of packets to simulate (default 20): {Style.RESET_ALL}")
        num_packets = int(num) if num.strip() else 20
    except ValueError:
        num_packets = 20
        
    stats, results = sim.run(num_packets)
    
    # 4. Visualization
    plot_stats(stats)
    
    print(f"\n{Fore.GREEN}{Style.BRIGHT}=== DEMONSTRATION COMPLETE ==={Style.RESET_ALL}")

if __name__ == "__main__":
    main()
