@echo off
@REM git subtree push --prefix github-page origin gh-pages
@REM First create worktree with git worktree add github-page gh-pages (Remember using admin powershell would cause problem)
cd github-page
git add *
git commit -m "Deploy updated GitHub Pages"
git push -uf origin gh-pages
pause