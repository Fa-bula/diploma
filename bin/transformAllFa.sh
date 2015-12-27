#!/bin/bash
for file in /home/bulat/diploma/genome/fa/*; do
    /home/bulat/diploma/bin/faTransform.py $file
done

