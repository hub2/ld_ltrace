# ld_ltrace

Implementation of fun idea that you can wrap all of the functions from shared libraries into one lib and use LD_PRELOAD to manipulate their behaviour. This one works by generating assembly code, then compiling it into libfake.so. At the moment, it prints name of every function it intercepts.

## Dependencies
- nasm
- gcc
- pyelftools (```pip install pyelftools```)

## Problems & ideas
- Displaying arguments of the functions? Is there a sane way to do it?
- Get rid of writing the assembly.
- Implement a way to get more control over the function behaviour(modifiying function result, args)


