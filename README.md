# League Match History Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Overview

The League Match History Analyzer is a sophisticated Python script designed to fetch and process player match history data from the Riot Games API. This versatile tool empowers gamers to gain valuable insights into their in-game performance and assess their win rates, enhancing their strategic decision-making abilities.

![Demo GIF](demo.gif)

## Key Features

- Seamless Integration: The application seamlessly integrates with the Riot Games API, providing access to detailed information about matches, champions, and player statistics.

- Win Rate Calculation: Advanced algorithms accurately calculate win rates, enabling players to assess their success rates in different game modes.

- Data Parsing and Filtering: Robust data parsing and filtering ensure efficient processing of raw data from the Riot API, focusing on relevant match outcomes and performance metrics.

- Command-Line Interface (CLI): The intuitive CLI allows users to input their summoner details easily and view detailed win rate statistics.

- Automated API Key Update (Optional): Optionally, the application can be configured to fetch a fresh API key daily from a secure external source, ensuring uninterrupted access to the Riot API.

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/your_username/League-Match-History-Analyzer.git
cd League-Match-History-Analyzer
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project directory and add your Riot Games API key:

```
API_KEY=your_riot_api_key_here
```

## Usage

Run the script and provide your in-game summoner name when prompted:

```bash
python match_history_analyzer.py
```

The application will fetch your match history data and display detailed win rate statistics for your recent games.

## How It Works

The "League Match History Analyzer" utilizes the Riot Games API to fetch match data for the provided summoner name. It then processes the data using data parsing and filtering algorithms to calculate win rates and other essential performance metrics. The application's command-line interface makes it easy for users to interact with the tool and explore their gaming statistics effortlessly.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- The League Match History Analyzer was created under Riot Games' "Legal Jibber Jabber" policy using assets owned by Riot Games. Riot Games does not endorse or sponsor this project.
- Thanks to Riot Games for providing the API and supporting the developer community.
- The application is built using Python and leverages the `python-dotenv` library for managing environment variables.

## Contributing

Contributions are welcome! If you'd like to improve the "League Match History Analyzer" please fork the repository and create a pull request. Feel free to open issues if you encounter bugs or have suggestions for new features.

Thanks!
-Albert Youssef
