
<a name="#top"></a>







<!-- PROJECT LOGO -->
<br />
<div align="center">
    <img src ="./docs/header_image_readme.jpeg">

  <h3 align="center">My Investment Assistant</h3>

  <p align="center">
  A Discord bot designed to to provide a weekly report of my investment holdings
  
  ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white) ![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)

  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#requirements">Requirements</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#bot-output">Bot Output</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

This goal of this project is to design a bot that notifies the user via a discord server of their:
- % returns for each stock in a given portfolio
- the total portfolio return
- The performance from the market (ASX 200)
- A written summary of the performance of each stock, and a comparison of the portfolio to the market.
- *If a stock price has reached a desired price on their watchlist (not yet implemented)*
- *News relating to their stocks and their watchlist (not yet implemented)*

<br>
<p align="right">(<a href="#top">back to top</a>)</p>

### Requirements
<br>

To run this code locally you need:

- A [ChatGPT API key](https://openai.com/blog/openai-api)
- A discord bot that has access to a server you would like messages to be sent to 
  - [tutorial](https://www.ionos.com/digitalguide/server/know-how/creating-discord-bot/)
- A storage solution, in this code i have used AWS S3 to hold my investment data in a csv
- Python
  - All python packages are in [requirements.txt](requirements.txt)


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage



<p align="right">(<a href="#top">back to top</a>)</p>


## Bot Output

screenshots of final product


<p align="right">(<a href="#top">back to top</a>)</p>
<!-- ROADMAP -->

## Roadmap

- [x] Create local version of code
- [x] Add ChatGPT interepretation
- [ ] Add latest news for stocks
- [ ] Add watchlist implementation
- [ ] Deploy solution either to home server or cloud



<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

Copyright 2023 James Bugden

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

 - [README Template](https://github.com/othneildrew/Best-README-Template/)
 - [discord.py Documentation](https://discordpy.readthedocs.io/en/stable/)
  
<p align="right">(<a href="#top">back to top</a>)</p>



