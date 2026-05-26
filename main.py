import os
import json
import csv
from simulation import run_simulation



# Run All Test Cases
def run_all_test_cases(folder_path):
    """
    Executes all JSON test cases in the folder.

    Parameters:
        folder path (str): Folder with all Test cases

    Returns:
        dict: final reports
    """
     
    final_report = {}

    # Get all JSON test files
    test_files = sorted([
        file for file in os.listdir(folder_path)
        if file.endswith(".json")
    ])

    if not test_files:
        print("No test cases found.")
        return final_report

    # Run each test case
    for file_name in test_files:

        file_path = os.path.join(
            folder_path,
            file_name
        )

        print(f"Running test case: {file_name}")

        try:

            # Run simulation
            report = run_simulation(file_path)

            # Store successful report
            final_report[file_name] = {
                "test_case_file": file_name,
                "status": "success",
                "report": report
            }

        except Exception as error:

            # Store failed report
            final_report[file_name] = {
                "test_case_file": file_name,
                "status": "failed",
                "error": str(error)
            }

            print(f"Error in {file_name}: {error}")

    return final_report



# Save Final Report
def save_report(report, output_file="report.json"):
    """
    Save and write report of Test case to a file 

    Parameters:
        report (dict):
            Final combined report.

        output_file (str):
            Output JSON filename.

    Returns: 
          None
    """

    with open(output_file, "w") as file:

        json.dump(
            report,
            file,
            indent=4
        )

    print(f"\nFinal report saved to '{output_file}'")




# Export Top Performers to CSV
def export_top_performers(final_report,
                          output_file="top_performers.csv"):
    """
    Export the best agent from each test case into the csv file
    Parameters:
        final_report (dict):
            Combined  report.

        output_file (str):
            Output CSV filename.

    Returns:
        None
    """

    with open(output_file, "w", newline="") as csv_file:

        writer = csv.writer(csv_file)

        # CSV Header
        writer.writerow([
            "Test Case File",
            "Best Agent"
        ])

        # Write data
        for test_case, result in final_report.items():

            if result["status"] == "success":

                best_agent = result["report"].get(
                    "best_agent",
                    "N/A"
                )

                writer.writerow([
                    test_case,
                    best_agent
                ])

    print(f"\nTop performers exported to '{output_file}'")



# Main Function
def main():
    """
    main function:

    workflow:
    load full test cases
    run simulation
    save json report 
    """

    folder_path = "Test cases"

    # Run all simulations
    final_report = run_all_test_cases(
        folder_path
    )

    # Save report
    save_report(final_report)

    # Export CSV
    export_top_performers(final_report)

    # # Print final report
    # print("\nFinal Combined Report:\n")

    # print(json.dumps(
    #     final_report,
    #     indent=4
    # ))


# -------------------------------------------------
# Driver Code
# -------------------------------------------------
if __name__ == "__main__":

    main()