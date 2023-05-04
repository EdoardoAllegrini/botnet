
<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/EdoardoAllegrini/botnet">
    <img src="images/logo_botnet.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Botnet</h3>

  <p align="center">
    A botnet architecture made by Command and Control (C&C) and some bots.
    <br />
    <br />
    ·
    <a href="https://github.com/EdoardoAllegrini/botnet/issues">Report Bug</a>
    ·
    <a href="https://github.com/EdoardoAllegrini/botnet/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
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
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Botnet occurs commonly in today's cyber attacks, resulting in serious threats to our network assets and organization's properties.
Botnets are collections of compromised computers (Bots) which are remotely controlled by a common command-and-control (C&C) infrastructure which is used to distribute commands to the Bots for malicious activities such as distributed denial-of-service (DDoS) attacks, sending large amount of SPAM and other nefarious purposes.
<br>
This tool can be used to simulate a botnet and control all the Bots by a single CLI offered by C&C. Using the CLI you can tell Bots to perform a bunch of cyber attacks:
- DDoS
- send email batch
- spoof software/hardware info about Bot


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python.org]][Python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

* python3
* mininet (not mandatory but for simulating a net)


### Installation


1. Clone the repo
   ```sh
   git clone https://github.com/EdoardoAllegrini/botnet
   ```
2. Install mininet (http://mininet.org/walkthrough/)
   ```sh
   cd ~
   git clone https://github.com/mininet/mininet  # if it's not already there
   mininet/util/install.sh -w
   ```
3. Give botnet/run_botnet.sh 'x' permission
   ```sh
   cd botnet
   chmod +x ./run_botnet.sh
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

1. Run the net:
   ```sh
   cd botnet
   ./run_botnet.sh
   ```
2. Open at least two terminals:
   ```sh
   mininet> xterm h1
   mininet> xterm h2
   ```
3. On h1 execute the Command an Control:
   ```sh
   cd CC
   python3 main.py
   ```
3. On other hosts (h2, ..., hx where x=6) execute the Bot:
   ```sh
   cd bot
   python3 main.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE.txt](LICENSE.txt) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Edoardo Allegrini - [website](https://EdoardoAllegrini.github.io)

Project Link: [https://github.com/EdoardoAllegrini/botnet](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[repo-url]: https://github.com/EdoardoAllegrini/botnet
[Python-url]: https://www.python.org
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
