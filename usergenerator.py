import urllib.request
import urllib.parse
import json
import random
import sys
import threading
import time
from queue import Queue, Empty

class AvisStyleUsernameGenerator:
    def __init__(self):
        self.users_url = "https://users.roblox.com"
        
        self.prefixes = [
            "un", "non", "anti", "pre", "post", "neo", "proto", "pseudo", "quasi",
            "semi", "ultra", "meta", "trans", "counter", "over", "under", "mis",
            "re", "de", "ex", "sub", "super", "hyper", "inter", "multi"
        ]
        
        self.core_words = [
            "ideal", "real", "sure", "certain", "fitting", "guttur", "elusor", "obsign",
            "legend", "optophone", "heronshaw", "maskal", "fewter",
            "lunar", "solar", "astral", "void", "echo", "ghost", "phantom", "shadow",
            "dream", "myth", "fable", "tale", "saga", "epic", "lore",
            "ocean", "river", "storm", "thunder", "lightning", "frost", "blaze",
            "ember", "crystal", "jade", "amber", "ivory", "ebony", "azure",
            "velvet", "silk", "satin", "lace", "pearl", "diamond", "opal",
            "zenith", "nadir", "apex", "vertex", "nexus", "vortex",
            "ism", "ness", "izes", "ises", "ling", "longe", "alism",
            "ine", "ity", "ance", "ence", "ment", "ship", "hood"
        ]
        
        self.suffixes = [
            "ism", "ness", "ity", "ize", "ise", "ing", "ed", "er", "or",
            "ling", "kin", "let", "ette", "ese", "esque", "ish", "ly",
            "ful", "less", "able", "ible", "ous", "ious", "eous", "al",
            "ial", "ic", "tic", "ive", "ative", "ive", "s", "es"
        ]
        
    def check_username_availability(self, username):
        try:
            url = f"https://auth.roblox.com/v1/usernames/validate?birthday=2000-01-01&context=Signup&username={urllib.parse.quote(username)}"
            req = urllib.request.Request(url, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode('utf-8'))
                code = result.get("code", -1)
                return {"available": code == 0, "code": code}
        except:
            return {"available": False, "code": -1}
    
    def generate_barcode(self, length=None):
        if length is None:
            length = random.randint(8, 18)
        return ''.join(random.choice(['I', 'l']) for _ in range(length))
    
    def generate_word_username(self, keywords=None):
        strategies = [
            lambda: random.choice(self.prefixes) + random.choice(self.core_words),
            lambda: random.choice(self.core_words) + random.choice(self.suffixes),
            lambda: random.choice(self.prefixes) + random.choice(self.core_words) + random.choice(self.suffixes),
            lambda: random.choice(self.core_words),
            lambda: random.choice(self.core_words) + random.choice(self.core_words),
            lambda: random.choice(keywords) if keywords else random.choice(self.core_words),
        ]
        return random.choice(strategies)().lower()
    
    def generate_5_letter(self):
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"
        return (
            random.choice(consonants) +
            random.choice(vowels) +
            random.choice(consonants) +
            random.choice(vowels) +
            random.choice(consonants)
        )
    
    def generate_5_character(self):
        return ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(5))
    
    def generate_4_letter(self):
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"
        return (
            random.choice(consonants) +
            random.choice(vowels) +
            random.choice(consonants) +
            random.choice(vowels)
        )
    
    def generate_4_character(self):
        return ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(4))
    
    def generate_3_letter(self):
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"
        return (
            random.choice(consonants) +
            random.choice(vowels) +
            random.choice(consonants)
        )
    
    def generate_3_character(self):
        return ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(3))
    
    def generate_6_letter(self):
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"
        return (
            random.choice(consonants) +
            random.choice(vowels) +
            random.choice(consonants) +
            random.choice(vowels) +
            random.choice(consonants) +
            random.choice(vowels)
        )
    
    def clean_username(self, username):
        allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
        cleaned = ''.join(c for c in username if c in allowed)
        while '__' in cleaned:
            cleaned = cleaned.replace('__', '_')
        cleaned = cleaned.strip('_')
        if cleaned and cleaned[0].isdigit():
            cleaned = 'x' + cleaned
        return cleaned[:20]

def worker_thread(generator, option, keywords, result_queue, stop_flag, checked_set, lock):
    while not stop_flag["stop"]:
        try:
            if option == "1": username = generator.generate_3_character()
            elif option == "2": username = generator.generate_3_letter()
            elif option == "3": username = generator.generate_3_letter() + "_"
            elif option == "4": username = generator.generate_3_character() + "_"
            elif option == "5": username = generator.generate_4_character()
            elif option == "6": username = generator.generate_4_letter()
            elif option == "7": username = generator.generate_4_letter() + "_"
            elif option == "8": username = generator.generate_4_character() + "_"
            elif option == "9": username = generator.generate_5_character()
            elif option == "10": username = generator.generate_5_letter()
            elif option == "11": username = generator.generate_5_letter() + "_"
            elif option == "12": username = generator.generate_5_character() + "_"
            elif option == "13": username = generator.generate_6_letter()
            elif option == "14": username = generator.generate_word_username(keywords)
            elif option == "15": username = generator.generate_barcode()
            else: username = generator.generate_word_username(keywords)

            username = generator.clean_username(username)
            if not (3 <= len(username) <= 20):
                continue

            with lock:
                if username in checked_set:
                    continue
                checked_set.add(username)

            result = generator.check_username_availability(username)
            if result["available"]:
                result_queue.put(username)
        except:
            pass

def main():
    print("=" * 70)
    print("ROBLOX USERNAME GENERATOR by 777")
    print("=" * 70)
    
    generator = AvisStyleUsernameGenerator()
    stop_flag = {"stop": False}

    # 👇 ENTER listener (FIXED)
    def listen_for_enter():
        input()
        stop_flag["stop"] = True

    print("\n📋 OPTIONS:")
    print("   [1]  3character    - 3 random characters")
    print("   [2]  3_letter      - 3-letter word-like")
    print("   [3]  3letter_      - 3-letter with underscore")
    print("   [4]  3character_   - 3-character with underscore")
    print("   [5]  4character    - 4 random characters")
    print("   [6]  4_letter      - 4-letter word-like")
    print("   [7]  4letter_      - 4-letter with underscore")
    print("   [8]  4character_   - 4-character with underscore")
    print("   [9]  5character    - 5 random characters")
    print("   [10] 5_letter      - 5-letter word-like")
    print("   [11] 5letter_      - 5-letter with underscore")
    print("   [12] 5character_   - 5-character with underscore")
    print("   [13] 6letter       - 6-letter word")
    print("   [14] word          - Aesthetic single word (Comma Wise Keywords supported)")
    print("   [15] barcode       - IIIIllllIlllllII style")
    
    option = input("\n➤ Select option (1-15): ").strip()
    
    keywords = None
    if option == "14":
        print("\n📝 Enter keywords for word generation (Comma Wise)")
        print("   Example: void, dream, ghost")
        keywords_input = input("➤ Keywords: ").strip()
        if keywords_input:
            keywords = [k.strip().lower() for k in keywords_input.split(",") if k.strip()]
    
    count = int(input("\n🔢 How many usernames to generate?: ").strip() or "1")
    
    print("\n⚡ Number of threads (more = faster, but don't overdo it)")
    print("   Recommended: 1-200 threads")
    num_threads = int(input("➤ Threads: ").strip() or "1")
    num_threads = max(1, min(num_threads, 200))
    
    print("\n⏸️  Press ENTER to stop the search\n")

    # 👇 start ENTER listener
    threading.Thread(target=listen_for_enter, daemon=True).start()
    
    result_queue = Queue()
    checked_set = set()
    lock = threading.Lock()
    
    workers = []
    for _ in range(num_threads):
        t = threading.Thread(
            target=worker_thread,
            args=(generator, option, keywords, result_queue, stop_flag, checked_set, lock),
            daemon=True
        )
        t.start()
        workers.append(t)
    
    available = []
    start_time = time.time()
    
    while len(available) < count and not stop_flag["stop"]:
        try:
            u = result_queue.get(timeout=0.2)
            available.append(u)
            elapsed = time.time() - start_time
            rate = len(checked_set) / elapsed if elapsed > 0 else 0
            print(f"[{len(available)}/{count}] ✅ {u} | Checked: {len(checked_set)} | Rate: {rate:.1f}/s")
        except Empty:
            pass
    
    stop_flag["stop"] = True
    for t in workers:
        t.join()
    
    print("\n📊 AVAILABLE USERNAMES\n")
    for u in available:
        print("   ✅", u)
    
    print(f"\n✨ Found {len(available)} usernames")
    print(f"⏱️  Time: {time.time() - start_time:.1f}s | Checked: {len(checked_set)}")

if __name__ == "__main__":
    while True:
        main()
        again = input("\n🔁 Generate again? (y/n): ").lower()
        if again != "y":
            break
