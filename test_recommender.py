# Tests that a pet is recommended based on the criteria

from recommender import calculate_suitability_score, Criteria, PET_DATA
#  Create test cases for the ff adopters:
# a. Couple looking for a pet - Both working fulltime in small apartment.
# b. Outdoor Person -  Enjoys hiking and camping. They want a furry companion that is energetic, adventurous, and good with outdoor activities.
# c. Allergy-Sensitive Individual - An individual with allergies is interested in adopting a hypoallergenic pet. They are looking for a pet that sheds minimally, requires little grooming, and is known to be less allergenic.

def calc_all_pet_suitability(situation:dict[Criteria, str]):
    return { pet: calculate_suitability_score(situation, PET_DATA[pet]) for pet in PET_DATA }

def test_recommends_cat_for_couple():
    couple_situation:dict[Criteria, str] = {
        Criteria.ENERGY_LEVEL: "Active",
        Criteria.INDEPENDENCE: "Little Attention",
        Criteria.LIVING_SPACE: "Small",
        Criteria.ENVIRONMENT_PREFERENCE: "Indoor",
        Criteria.PET_CARE: "Low"
    }
    scores = calc_all_pet_suitability(couple_situation)

    # print(scores)
    # Check if cat is recommended
    assert scores["cat"] > scores["dog"], "Cat should be recommended over dog"
    assert scores["cat"] > scores["rabbit"], "Cat should be recommended over rabbit"

def test_recommends_dog_for_outdoor_person():
    outdoor_person_situation:dict[Criteria, str] = {
        Criteria.ENERGY_LEVEL: "Very Active",
        Criteria.INDEPENDENCE: "Moderate Attention",
        Criteria.LIVING_SPACE: "Large",
        Criteria.ENVIRONMENT_PREFERENCE: "Outdoor",
        Criteria.PET_CARE: "High"
    }

    scores = calc_all_pet_suitability(outdoor_person_situation)

    # Check if dog is recommended 
    assert scores["dog"] > scores["cat"], "Dog should be recommended over cat"
    assert scores["dog"] > scores["rabbit"], "Dog should be recommended over rabbit"

def test_recommends_rabbit_for_allergy_sensitive_individual():
    allergy_sensitive_situation:dict[Criteria, str] = {
        Criteria.ENERGY_LEVEL: "Inactive",
        Criteria.INDEPENDENCE: "Moderate Attention",
        Criteria.LIVING_SPACE: "Small",
        Criteria.ENVIRONMENT_PREFERENCE: "Indoor",
        Criteria.PET_CARE: "Moderate"
    }
    scores = calc_all_pet_suitability(allergy_sensitive_situation)

    # Check if rabbit is recommended
    assert scores["rabbit"] > scores["cat"], "Rabbit should be recommended over cat"
    assert scores["rabbit"] > scores["dog"], "Rabbit should be recommended over dog"
