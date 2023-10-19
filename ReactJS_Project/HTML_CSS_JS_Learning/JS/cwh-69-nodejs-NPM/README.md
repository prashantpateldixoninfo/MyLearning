## Initialize the NPM package
    $npm init
    $npm install express
    $npm install slugify
    $npm install nodemon --global
    $npm view slugify version

## Versioning system(Notation)
    `version 2.3.0 [major minor patch]`

    `^2.3.0 — [Caret Symbol] This tells npm to upgrade to minor and patch versions, but not major versions. So, basically 2.3.4, 2.3.9, 2.4.5, 2.8 but not 3.0.0 onwards. (Upgrade to minor and patch, but not major)`

    `~2.3.0 — [Tilde Symbol] This tells npm to upgrade to patch versions, but not minor and major versions. So 2.3.4, 2.3.9 but not 2.4.0 onwards. (Upgrade to patch, but not minor and major)`
