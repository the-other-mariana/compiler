# Compiler & Its Theory

This repo contains a basic compiler for an arbitrary grammar. Its development is based on the theory and principles found in the book:

- [Compilers - Principles, Techniques, and Tools-Pearson_Addison Wesley (2006)](https://github.com/the-other-mariana/compiler/blob/master/book/Alfred%20V.%20Aho%2C%20Monica%20S.%20Lam%2C%20Ravi%20Sethi%2C%20Jeffrey%20D.%20Ullman-Compilers%20-%20Principles%2C%20Techniques%2C%20and%20Tools-Pearson_Addison%20Wesley%20(2006).pdf) by Alfred V. Aho, Monica S. Lam, Ravi Sethi, Jeffrey D. Ullman. It is the first pdf shown in the [book](https://github.com/the-other-mariana/compiler/tree/master/book) folder.

## Remove Large Files Wrongly Committed

```
git filter-branch -f --tree-filter 'rm -rf path/to/your/file' HEAD
git push
```

- Source: https://thomas-cokelaer.info/blog/2018/02/git-how-to-remove-a-big-file-wrongly-committed/