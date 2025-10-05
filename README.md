# Ceylonicus-Programming-Language
<p align="center">
    <img width="1200px" src="https://ceylonicus.vercel.app/css/logo-1200x268.png"><br/>
  </a>
</p>

# The First Sinhala Programming Language

**Ceylonicus** is the **first programming language to support Sinhala language syntax**, while also supporting English syntax seamlessly. This aims to make programming more accessible to Sinhala speakers. This project is a **prototype/model language**

- Author: Yehan Wasura

## Sinhala & English in unified codebase

Ceylonicus allows you to write both **Sinhala and English code** in the same source file. This flexibility makes it easy for users transitioning from English-based programming or mixing native terms with global standards.

**Example:**

```
විචල්‍ය අංකයක් = 10
write(අංකයක්)
```

This will output:
`10`

You can freely combine Sinhala identifiers and English functions or vice versa. There's no syntax conflict when mixing the two.
## Naming Inspiration

The name **Ceylonicus** comes from [_Bungarus ceylonicus_](https://en.wikipedia.org/wiki/Bungarus_ceylonicus), is a species of [venomous](https://en.wikipedia.org/wiki/Venomous "Venomous") [elapid](https://en.wikipedia.org/wiki/Elapidae "Elapidae") snake which is endemic to Sri Lanka. It also acknowledges that the language was **prototyped using Python**.

Experience Ceylonicus instantly: [**Launch Ceylonicus Web IDE**](https://ceylonicus.vercel.app/)

## Get Started with Ceylonicus

Ceylonicus offers multiple  ways to run your code. Choose the method that best suits your workflow:

### Method 1: Local Setup (Python & PyQt5)

For a powerful local development experience with a graphical user interface:

1. **Clone this repository:**

    ```
    git clone https://github.com/RezSat/Ceylonicus.git
    cd Ceylonicus
    ```
    
2. **Ensure Python and PyQt5 are installed.**
3. **Run the GUI IDE:**

    ```
    python IDE.py
    ```
    
    Alternatively, for command-line execution:

    ```
    python main.py your_file.cyl
    ```
    
    _(Use the appropriate Python command for your operating system.)_

### Method 2: Windows Executable

The simplest way to get started on Windows:

1. **Download the latest executable** from the [releases page](https://www.google.com/search?q=https://github.com/RezSat/Ceylonicus/releases).
2. **Execute your Ceylonicus file** directly from your command prompt:
    
    ```
    {path_to_executable}\ceylonicus.exe {your_file.cyl}
    ```
    
    **Example:**
    
    ```
    ceylonicus.exe test.cyl
    ```
    

### Method 3: Ceylonicus Web IDE (Browser-Based)

Code and run Ceylonicus directly in your web browser, no installation required!

- Visit the [**Ceylonicus Web IDE**](https://ceylonicus.vercel.app/) This is made possible by [Brython](https://brython.info/), enabling Python to run directly in the browser.

---

## Explore Examples

Dive into language of Ceylonicus. You can find various code examples demonstrating the language's features within the `examples` folder, or if you use the web ide you can also find them under Examples tab.
