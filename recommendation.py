def get_recommendations(crack_length, object_type):
    recommendations = {
        "repair": [],
        "leakage_risks": [],
        "object": object_type,
        "severity": "",
    }

    # Crack severity and recommendations based on object type
    if crack_length < 500:
        recommendations["severity"] = "Minor"
        recommendations["repair"].append("Apply a sealant and monitor for changes.")
        
        if object_type == "wall":
            recommendations["leakage_risks"].append("No immediate leakage, but periodic inspection is advised.")
        elif object_type == "water tank":
            recommendations["leakage_risks"].append("Minimal risk of water leakage, but monitor for crack growth.")
        elif object_type == "chemical tank":
            recommendations["leakage_risks"].append("Low chance of chemical leakage, but apply protective coating.")

    elif 500 <= crack_length < 2000:
        recommendations["severity"] = "Moderate"
        recommendations["repair"].append("Fill the crack with epoxy or grout.")
        
        if object_type == "wall":
            recommendations["leakage_risks"].append("Possible risk of moisture leakage and wall deterioration.")
        elif object_type == "water tank":
            recommendations["leakage_risks"].append("Increased chance of water leakage if untreated.")
        elif object_type == "chemical tank":
            recommendations["leakage_risks"].append("Moderate risk of hazardous chemical leakage if untreated.")

    else:
        recommendations["severity"] = "Severe"
        recommendations["repair"].append("Seek professional repair services immediately.")
        
        if object_type == "wall":
            recommendations["leakage_risks"].append("High chance of structural failure, risking wall collapse.")
        elif object_type == "water tank":
            recommendations["leakage_risks"].append("High risk of severe water leakage and contamination.")
        elif object_type == "chemical tank":
            recommendations["leakage_risks"].append("Critical risk of chemical leaks with possible environmental harm.")

    return recommendations
