#!/bin/bash
for file in /home/bulat/projects/diploma/genome/fa/*; do
    /home/bulat/projects/diploma/bin/faTransform.py $file
done

