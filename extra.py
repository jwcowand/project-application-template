  # ### TIME SERIES ANALYSIS: Issue Activity in 2023
        # # Convert `created_at` to datetime if it isn't already
        # issues_df['created_at'] = pd.to_datetime(issues_df['created_at'], errors='coerce')  # Ensure datetime format

        # # Filter for issues created in the year 2023
        # issues_2023 = issues_df[issues_df['created_at'].dt.year == 2023]

        # # Resample by month to count the number of issues created each month in 2023
        # issues_over_2023 = issues_2023.set_index('created_at').resample('M').size()

        # # Plotting issue creation trend over the 12 months of 2023
        # plt.figure(figsize=(12, 6))
        # ax = issues_over_2023.plot(kind='line', color="#2a9d8f", marker='o')
        # plt.title("Monthly Trend of Issue Creation in 2023")
        # plt.xlabel("Month")
        # plt.ylabel("Number of Issues Created")
        # plt.grid(True, linestyle='--', alpha=0.7)

        # # Set date format on the x-axis to show months
        # date_format = DateFormatter("%b")  # Format to show only month (e.g., Jan, Feb)
        # ax.xaxis.set_major_formatter(date_format)

        # # Adjust the layout for better appearance
        # plt.tight_layout()
        # plt.show()