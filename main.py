import os
import random
import sys
import threading
import time
from typing import List, Tuple, Optional

import wikipedia
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- Configuration and Constants ---

# ANSI Colors for console output
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"
HEADER = '\033[95m'
UNDERLINE = '\033[4m'

# Dictionary of topics categorized by subject
TOPICS_BY_CATEGORY = {
    "lifestyle": [
        "Cooking", "Fashion", "Film", "Music", "Yoga", "Gardening"
    ],
    "science": [
        "Photosynthesis", "Black hole", "DNA", "Gravitational wave",
        "Theory of relativity", "Volcano", "Quantum computing"
    ],
    "politics": [
        "Democracy", "Socialism", "Capitalism", "Communism",
        "Monarchy", "Republic"
    ]
}

# Threading event to signal the animation to stop
stop_event = threading.Event()


# --- Display Functions ---

def print_logo() -> None:
    """Prints the game's ASCII logo with dynamic colors and separation."""
    print(f"{BLUE}"
          "================================================================="
          f"======{RESET}")
    print(rf"""{BLUE}{BOLD}
  ███████╗ █████╗ ██╗  ██╗███████╗    ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗
  ██╔════╝██╔══██╗██║ ██╔╝██╔════╝    ██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
  █████╗  ███████║█████╔╝ █████╗      █████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
  ██╔══╝  ██╔══██║██╔═██╗ ██╔══╝      ██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
  ██║     ██║  ██║██║  ██╗███████╗    ██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
{RESET}{YELLOW}
         {BOLD}🕵️‍♂️ Facts from Wikipedia, Fakes by Gemini!{RESET}
         """)
    print(f"{BLUE}"
          "================================================================="
          f"======{RESET}")


def print_welcome_message() -> None:
    """Prints the initial welcome banner with color and flair."""
    print(f"\n{HEADER}{BOLD}⭐️ Welcome to FAKE FINDER! Test Your Knowledge! ⭐️{RESET}")
    print(f"{CYAN}--- Get Ready to Begin ---{RESET}")


def print_display_score(name: str, score: int, round_number: int) -> None:
    """Prints the current score after each round."""
    print(f"\n{BOLD}{CYAN}PLAYER:{RESET} {name} | {BOLD}{CYAN}FINAL ROUND SCORE:{RESET} "
          f"{score}/{round_number}")
    print("_________________________________________________________________")


def animate() -> None:
    """
    Displays a text animation with a detective emoji while the API call is
    running. Stops when the global stop_event is set.
    """
    detective_emoji = [
        "🔍(•‿•)", " 🔍( •‿•)", "  🔍(  •‿•", "   🔍(   •‿•",
        "   🔍(   -‿-", "  🔍(  •‿•", " 🔍( •‿•)", "🔍(•‿•)"
    ]
    # Cycle through a random pair of emojis for variety
    for c in random.choice(list(zip(*[iter(detective_emoji)] * 2))):
        if stop_event.is_set():
            break
        sys.stdout.write('\rSearching for facts ... ' + c)
        sys.stdout.flush()
        time.sleep(0.3)
    sys.stdout.write('\r')


# --- Game Logic and Input Functions ---

def get_user_input() -> Tuple[str, str, int]:
    """
    Prompts the user for their name, game level, and number of rounds.

    Returns:
        A tuple containing (name, level, rounds).
    """
    print(f"\n{YELLOW}--- Player Setup ---{RESET}")

    user_input_name = input(f"{BOLD}{CYAN}👤 Enter your name: {RESET}")

    while True:
        user_input_level = input(
            f"{BOLD}{BLUE}🕹️ Choose difficulty (Easy{RESET}/{YELLOW}Medium{RESET}/"
            f"{RED}Hard{BLUE}): {RESET}"
        ).strip().lower()
        if user_input_level in ["easy", "medium", "hard"]:
            break
        print(f"{RED}❌ Please enter 'easy', 'medium', or 'hard'.{RESET}\n")

    while True:
        try:
            user_input_rounds = int(input(
                f"{BOLD}{CYAN}🔢 How many rounds (1-10)?: {RESET}"
            ).strip())
            if 1 <= user_input_rounds <= 10:
                break
            print(f"{RED}❌ Please enter a number between 1 and 10.{RESET}\n")
        except ValueError:
            print(f"{RED}❌ Please enter a valid number.{RESET}\n")

    return user_input_name, user_input_level, user_input_rounds


def get_user_category() -> List[str]:
    """
    Prompts the user to select a game category.

    Returns:
        A list of topic strings for the selected category.
    """
    print(f"\n{YELLOW}"
          "================================================================="
          f"======{RESET}")
    print(f"{HEADER}{BOLD}📚 Choose Your Challenge Category:{RESET}")
    print(f"{CYAN}1. Lifestyle{RESET}")
    print(f"{YELLOW}2. Science{RESET}")
    print(f"{BLUE}3. Politics{RESET}")
    print(f"{YELLOW}"
          "================================================================="
          f"======{RESET}")

    while True:
        user_input_category = input(
            f"{BOLD}{HEADER}➡️ Provide your choice (1/2/3): {RESET}"
        ).strip()

        if user_input_category in ["1", "2", "3"]:
            key = list(TOPICS_BY_CATEGORY.keys())[
                int(user_input_category) - 1
            ]
            return TOPICS_BY_CATEGORY[key]

        print(f"{RED}❌ Invalid input. Please enter 1, 2, or 3.{RESET}\n")


def get_user_topics(topics: List[str]) -> str:
    """
    Prompts the user to select a specific topic from the provided list.

    Args:
        topics: A list of available topics in the chosen category.

    Returns:
        The selected topic string.
    """
    print(f"{CYAN}--- Topic Selection ---{RESET}")
    print(f"{BOLD}Choose a specific topic to begin the round:{RESET}")

    list_index = []
    for index, topic in enumerate(topics):
        # Use GREEN for the index and YELLOW for the topic
        print(f"{GREEN}{index + 1}.{RESET} {YELLOW}{topic}{RESET}")
        list_index.append(index + 1)

    while True:
        try:
            user_input_topic = input(
                f"{BOLD}{BLUE}➡️ Select one number: {RESET}"
            ).strip()
            topic_index = int(user_input_topic)
            if topic_index in list_index:
                return topics[topic_index - 1]

            print(f"{RED}❌ Please enter a valid number from the list.{RESET}\n")

        except ValueError:
            print(f"{RED}❌ Please enter a number.{RESET}\n")


def get_article_from_wikipedia(title: str) -> str:
    """
    Retrieves the full content of a Wikipedia article given its title.

    Args:
        title: The title of the Wikipedia page.

    Returns:
        The full content of the Wikipedia article as a string.
    """
    try:
        # Fixed: Removed 'auto_suggest=True'
        page = wikipedia.WikipediaPage(title=title)
        return page.content
    except (wikipedia.exceptions.PageError,
            wikipedia.exceptions.DisambiguationError) as e:
        print(f"{RED}Error fetching Wikipedia article for '{title}': {e}{RESET}")
        return ""


def generate_facts(article_content: str, level: str) -> str:
    """
    Generates true and fake facts using the Gemini API.

    Args:
        article_content: The source text from Wikipedia.
        level: The difficulty level ('easy', 'medium', or 'hard').

    Returns:
        A pipe-separated string of facts and their boolean status from Gemini.
    """
    # Start animation thread
    stop_event.clear()
    animation_thread = threading.Thread(target=animate)
    animation_thread.start()

    # Load environment variables (including GEMINI_API_KEY)
    load_dotenv()

    try:
        # Initialize Gemini Client (automatically uses GEMINI_API_KEY)
        client = genai.Client()

        # PEP 8 compliant prompt string using line continuations
        full_prompt = (
            "# Inputs:\n"
            f"The content of the article is: {article_content}\n\n"
            f"The selected level is: {level}\n\n"
            "# Role\n"
            "You are part of a game called Fake Finder. A fact checking "
            "game that provides real facts and one fake fact.\n\n"
            "# Goal\n"
            "Select 3 factual sentences that are present in the article. "
            "Generate 1 wrong fake sentence based on a fourth one from the "
            "article.\n\n"
            "# Rules\n"
            "- The fake sentence should always be the first sentence.\n"
            "- The Fake sentence should be followed by boolean \"False\".\n"
            "- The Factual sentences should be followed by boolean \"True\".\n"
            "- The sentences should not have more than 25 words.\n"
            "- Do not hallucinate or generate random factual sentences.\n"
            "- Focus only on the given input text.\n"
            "- The level defines the complexity of the sentences:\n"
            "  - easy = A simple sentence that is clearly true or false.\n"
            "  - medium = A fact that requires moderate knowledge.\n"
            "  - hard = A challenging fact where the fake is subtle.\n\n"
            "# Output Format:\n"
            "(fake_sentence @ False) | (fact_sentence_1 @ True) | "
            "(fact_sentence_2 @ True) | (fact_sentence_3 @ True)"
        )

        # Call Gemini API
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt,
            config=types.GenerateContentConfig(
                temperature=0.7
            )
        )

        # Stop animation
        stop_event.set()
        animation_thread.join()

        return response.text

    except Exception as e:
        # Stop animation and exit gracefully on API error
        stop_event.set()
        animation_thread.join()
        print(f"\n{RED}An error occurred with the Gemini API call: {e}{RESET}")
        print(f"{RED}Ensure GEMINI_API_KEY is set and the model is available."
              f"{RESET}")
        sys.exit(1)


def convert_string_to_list(fact_string: str) -> List[Tuple[str, bool]]:
    """
    Parses the pipe-separated string from the Gemini API into a list of
    fact-boolean tuples.

    Args:
        fact_string: The output string from the generate_facts function.

    Returns:
        A list of tuples: [(sentence, is_true), ...].
    """
    result = []
    # Split by the pipe | delimiter
    items = fact_string.strip().split("|")
    for item in items:
        # Find the delimiter @
        parts = item.split("@")
        if len(parts) == 2:
            # Extract sentence (strip whitespace and parentheses)
            sentence = parts[0].strip().lstrip('(').strip()
            # Extract boolean (strip whitespace and parentheses)
            boolean_str = parts[1].strip().rstrip(')').strip()

            is_true = boolean_str.lower() == "true"
            result.append((sentence, is_true))

    # Validate output length
    if len(result) != 4:
        # Return only complete, well-formed items
        return [item for item in result if item[0] and
                isinstance(item[1], bool)]

    return result


def display_randomized_facts(
    facts: List[Tuple[str, bool]]
) -> List[Tuple[str, bool]]:
    """
    Randomizes the order of facts and displays them to the user.

    Args:
        facts: A list of (sentence, boolean) tuples.

    Returns:
        The randomized list of facts.
    """
    if not facts:
        return []

    print("_________________________________________________________________")
    print(f"{BOLD}{HEADER}🔍 Which of these four statements is a FAKE story?{RESET}")

    # Randomize the fact list
    random.shuffle(facts)

    # Display facts in the console
    for index, (fact, _) in enumerate(facts):
        print(f"{GREEN}{BOLD}{index + 1}.{RESET} {fact}")

    return facts


def check_answer(facts: List[Tuple[str, bool]]) -> Optional[bool]:
    """
    Prompts the user for their answer and checks if it's correct.

    Args:
        facts: The randomized list of (sentence, boolean) tuples.

    Returns:
        True if the answer is correct, False otherwise. Returns None if the
        input facts list is empty.
    """
    if not facts:
        return None

    while True:
        try:
            user_answer = input(
                f"{BOLD}{YELLOW}➡️ Enter the number (1/2/3/4): {RESET}"
            ).strip()

            if 1 <= int(user_answer) <= 4:
                break
            print(f"{RED}❌ Please enter a valid number (1 to 4).{RESET}")

        except ValueError:
            print(f"{RED}❌ Please enter a number.{RESET}")

    # Find the index and text of the fake sentence (where boolean is False)
    correct_sentence = ""
    correct_index = -1
    for index, fact_tuple in enumerate(facts):
        if not fact_tuple[1]:
            correct_index = index
            correct_sentence = fact_tuple[0]
            break

    # Check the user's answer against the correct index
    if int(user_answer) - 1 == correct_index:
        print(f"\n{GREEN}{BOLD}🎉 That's CORRECT! You found the fake fact! {RESET}")
        return True
    else:
        print(f"\n{RED}{BOLD}🚫 Sorry, that's INCORRECT.{RESET}")
        print("\nThe fake sentence was:")
        print(f'{CYAN}"{correct_sentence}"{RESET}')
        return False


# --- Main Execution ---

def main():
    """Main function to run the Fake Finder game loop."""
    print_logo()
    print_welcome_message()

    while True:
        user_name, user_level, user_rounds = get_user_input()
        score = 0

        for round_num in range(1, user_rounds + 1):
            print(f"\n{YELLOW}"
                  "============================== ROUND "
                  f"{round_num}/{user_rounds} =============================={RESET}")
            print(f"{BOLD}{CYAN}PLAYER:{RESET} {user_name} | {BOLD}{CYAN}LEVEL:{RESET} "
                  f"{user_level} | {BOLD}{CYAN}CURRENT SCORE:{RESET} {score}")

            # 1. Get category and topic from user
            topic_list = get_user_category()
            title = get_user_topics(topic_list)
            print(f"\n{BOLD}Topic Selected: {YELLOW}{title}{RESET}")

            # 2. Get article content from Wikipedia
            print(f"\n{CYAN}--- Retrieving article on {title} ---{RESET}")
            article_content = get_article_from_wikipedia(title)

            if not article_content:
                print(f"{RED}Skipping this round due to Wikipedia error.{RESET}")
                continue

            # 3. Generate facts using Gemini
            raw_facts = generate_facts(article_content, user_level)
            transformed_facts = convert_string_to_list(raw_facts)

            if len(transformed_facts) != 4:
                print(f"{RED}Skipping: AI failed to generate 4 valid facts. "
                      f"Try a different topic.{RESET}")
                continue

            # 4. Display randomized facts
            randomized_facts = display_randomized_facts(transformed_facts)

            # 5. Check answer and update score
            is_correct = check_answer(randomized_facts)
            if is_correct is True:
                score += 1

            print_display_score(user_name, score, round_num)

        # Game end message
        print(f"\n{CYAN}"
              "================================== GAME OVER "
              f"======================================{RESET}")
        print(f"{BOLD}{GREEN}FINAL SCORE:{RESET} {score}/{user_rounds}!")

        quit_message = input(
            f"{BOLD}{YELLOW}\nWould you like to play again? (Y/N): {RESET}"
        ).strip().upper()
        if quit_message in ("N", "NO"):
            print(f"\n{HEADER}Thank you for playing Fake Finder! Goodbye!{RESET}")
            break


if __name__ == "__main__":
    main()