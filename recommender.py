# A pet recommender system that uses fuzzy logic to recommend a pet based on the adopter's preferences and a pet's characteristics.

# Based on the circumstances originally given,the following criteria are used to recommend a pet:
# 1. Energy Level
# 2. Independence
# 3. Living Space
# 4. Environment Preference
# 5. Pet Care
#  Use the following membership functions for each of the criteria:

# A given category has an exclusive interval, meaning:
# "category": [inclusive min, exclusive max]
import enum

class Criteria(enum.Enum):
    ENERGY_LEVEL = 0
    INDEPENDENCE = 1
    LIVING_SPACE = 2
    ENVIRONMENT_PREFERENCE = 3
    PET_CARE = 4

MEMBERSHIP_FX: dict[Criteria, dict[str, tuple[float, float]]] = {
    Criteria.ENERGY_LEVEL: {
        "Very Inactive": (0,0.2),
        "Inactive": (0.2,0.4),
        "Active": (0.4,0.7),
        "Very Active": (0.7,1)
    },
    Criteria.INDEPENDENCE: {
        "Little Attention": (0, 0.2),
        "Some Attention": (0.2,0.4),
        "Moderate Attention": (0.4,0.8),
        "Constant Attention": (0.8,1)
    },
    Criteria.LIVING_SPACE: {
        "Small": (0, 0.3),
        "Medium": (0.3,0.7),
        "Large": (0.7, 1)
    },
    Criteria.ENVIRONMENT_PREFERENCE:{
        "Indoor": (0, 0.33),
        "Either": (0.33, 0.67), # "either" means "either indoor or outdoor"
        "Outdoor": (0.67, 1)
    },
    Criteria.PET_CARE: {
        "Low": (0, 0.33),
        "Moderate": (0.33, 0.67),
        "High": (0.67, 1)
    }
}

# Warning: Arbitrary pet data
PET_DATA:dict[str, dict[Criteria,float]] = {
    "cat": {
        Criteria.ENERGY_LEVEL: 0.6, # active
        Criteria.INDEPENDENCE: 0.2, # some attention
        Criteria.LIVING_SPACE: 0.4, # small
        Criteria.ENVIRONMENT_PREFERENCE: 0.5, # indoor
        Criteria.PET_CARE: 0.3, # low
    },
    "dog": {
        Criteria.ENERGY_LEVEL: 0.8, # very active
        Criteria.INDEPENDENCE: 0.6, # moderate attention
        Criteria.LIVING_SPACE: 0.65, # medium
        Criteria.ENVIRONMENT_PREFERENCE: 0.75, # either
        Criteria.PET_CARE: 0.6, # high
    },
    "rabbit": {
        Criteria.ENERGY_LEVEL: 0.4, # active
        Criteria.INDEPENDENCE: 0.6, # moderate attention
        Criteria.LIVING_SPACE: 0.25, # small
        Criteria.ENVIRONMENT_PREFERENCE: 0.4, # either
        Criteria.PET_CARE: 0.7, # moderate
    },
}
# a. Couple looking for a pet - Both working fulltime in small apartment.
# b. Outdoor Person -  Enjoys hiking and camping. They want a furry companion that is energetic, adventurous, and good with outdoor activities.
# c. Allergy-Sensitive Individual - An individual with allergies is interested in adopting a hypoallergenic pet. They are looking for a pet that sheds minimally, requires little grooming, and is known to be less allergenic.

def curried_ask_criteria(prompt:str, scale:float):
    if scale <= 0:
        raise ValueError("Scale must be greater than 0")
    
    def ask_criteria() -> float:
        ans = input(prompt)
        try:
            percentage = float(ans)/scale
            if percentage < 0 or percentage > 1:
                return ask_criteria()
            return percentage
        except ValueError:
            return ask_criteria()
    return ask_criteria

ask_energy_level = curried_ask_criteria("From a scale of 1 to 10, how active do you want your pet to be?\n(1 to 10): ", 10)
HOURS_PER_DAY  = 24
ask_away_time = curried_ask_criteria("In a day, how many hours are you usually away from home?\n(0 to 24): ", HOURS_PER_DAY)
ask_environment_preference = curried_ask_criteria("From a scale of 1 to 10, do you prefer an indoor or outdoor pet?\n (1 to 10): ", 10)
ask_living_space = curried_ask_criteria("From a scale of 1 to 10, 1 being small and 10 being large, how much space do you have at home?\n(1 to 10): ", 10)
ask_pet_care = curried_ask_criteria("From a scale of 1 to 10, do you want a pet that sheds regularly and require grooming?\n (1 - rarely sheds and little to no grooming and 10 - sheds regularly and constant grooming): ", 10)

def fuzzify(key:Criteria, value:float) -> str:
    for category, interval in MEMBERSHIP_FX[key].items():
        if interval[0] <= value <= interval[1]:
            return category
    raise KeyError(f"{value} not in any category")

def calculate_suitability_score(adopter_preferences:dict[Criteria, str], pet:dict[Criteria, float], decimal_places_accuracy:int=2) -> float:
    score = 0
    for criterion, preference in adopter_preferences.items():
        membership_fx = MEMBERSHIP_FX[criterion]
        for category, interval in membership_fx.items():
            if preference == category:
                min_val, max_val = interval
                break
        pet_value = pet[criterion]
        if pet_value >= min_val and pet_value <= max_val:
            score += 1
    return round(score/len(adopter_preferences), decimal_places_accuracy)

def main():
    '''Run if main module'''
    print("Welcome to Pet Recommender!")
    print("We will ask you some questions to identify the most suitable pet for you.\n")

    adopter_scores = {
        Criteria.ENERGY_LEVEL: ask_energy_level(),
        Criteria.INDEPENDENCE: ask_away_time(),
        Criteria.LIVING_SPACE: ask_living_space(),
        Criteria.ENVIRONMENT_PREFERENCE: ask_environment_preference(),
        Criteria.PET_CARE: ask_pet_care()
    }
    adopter_preference = {
        criterion: fuzzify(criterion, score) for criterion, score in adopter_scores.items()
    }

    # Analysis
    print("Pets that have the following characteristics may fit your situation:")
    for criterion, preference in adopter_preference.items():
        print(f"{criterion.name.replace('_',' ').title()}: {preference.title()} ({adopter_scores[criterion]})")

    # Recommendation
    print(f"\nSearching knowledge base...")
    
    recommendation = max(PET_DATA, key=lambda pet: calculate_suitability_score(adopter_preference, PET_DATA[pet]))
    print(f"Recommended Pet: {recommendation}")
    print_suitability(recommendation, adopter_preference)

    # Show Pet Criteria
    print(f"A {recommendation} has the following characteristics:")
    show_pet_criteria(recommendation)

    # Show other pets
    print("\nOther pets:")
    for pet in PET_DATA:
        if pet != recommendation:
            print(f"{pet}:")
            print_suitability(pet, adopter_preference)
            show_pet_criteria(pet)
            print("\n")

def print_suitability(pet:str, adopter_preference:dict[Criteria, str]):
    print(f"Suitability: {calculate_suitability_score(adopter_preference, PET_DATA[pet])*100}%")
def show_pet_criteria(pet:str):
    for criterion, value in PET_DATA[pet].items():
        print(f"{criterion.name.replace('_',' ').title()}: {fuzzify(criterion, value).title()} ({value})")
if __name__ == '__main__':
    main()
