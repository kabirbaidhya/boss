#!/bin/bash

if [ -z "$NEXT" ]; then
    NEXT="Next"
fi

echo "Generating change log upto version: $NEXT"
github_changelog_generator --pr-label "**Improvements:**" --issue-line-labels=ALL --future-release="$NEXT"

