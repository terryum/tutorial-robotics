-- macOS fallback for guided learning when browser connector tools are unavailable.
-- Prefer scripts/open_lesson.py, which saves the returned tab/language receipt.
on languageForURL(pageURL)
    if pageURL starts with "https://github.com/terryum/tutorial-robotics/blob/main/docs/ko/" then return "ko"
    if pageURL starts with "https://github.com/terryum/tutorial-robotics/blob/main/docs/en/" then return "en"
    return ""
end languageForURL

on run argv
    if (count of argv) < 2 or (count of argv) > 4 then error "Provide fallback language, lesson ID, optional tab ID and preserve/force mode."
    set lessonLanguage to item 1 of argv
    set lessonID to item 2 of argv
    set preferredTabID to ""
    set languageMode to "preserve"
    if (count of argv) > 2 then set preferredTabID to item 3 of argv
    if (count of argv) > 3 then set languageMode to item 4 of argv
    if languageMode is not in {"preserve", "force"} then error "Language mode must be preserve or force."
    if lessonLanguage is not in {"ko", "en"} then error "Language must be ko or en."
    if lessonID is "" then error "Lesson ID is required."
    repeat with c in characters of lessonID
        if contents of c is not in "abcdefghijklmnopqrstuvwxyz0123456789-" then error "Invalid lesson ID."
    end repeat
    set docsPrefix to "https://github.com/terryum/tutorial-robotics/blob/main/docs/"
    tell application "Google Chrome"
        set selectedTab to missing value
        set selectedWindow to missing value
        set selectedIndex to 0
        set reused to false
        -- Prefer the recorded tab; otherwise keep the first matching tab.
        -- Chrome lists the front window first, so its active tutorial tab wins a tie.
        repeat with w in windows
            set tabNumber to 0
            repeat with t in tabs of w
                set tabNumber to tabNumber + 1
                if my languageForURL(URL of t) is not "" then
                    if selectedTab is missing value or ((id of t as text) is preferredTabID) or (selectedWindow is w and tabNumber is active tab index of w and (id of selectedTab as text) is not preferredTabID) then
                        set selectedTab to t
                        set selectedWindow to w
                        set selectedIndex to tabNumber
                    end if
                    set reused to true
                end if
            end repeat
        end repeat
        if reused then
            if languageMode is "preserve" then set lessonLanguage to my languageForURL(URL of selectedTab)
            set active tab index of selectedWindow to selectedIndex
            set index of selectedWindow to 1
        end if
        set lessonURL to docsPrefix & lessonLanguage & "/lessons/" & lessonID & ".md"
        if not reused then
            if (count of windows) is 0 then make new window
            tell front window
                set selectedTab to make new tab at end of tabs with properties {URL:lessonURL}
                set active tab index to count of tabs
            end tell
        else
            if URL of selectedTab is not lessonURL then set URL of selectedTab to lessonURL
        end if
        activate
        repeat 40 times
            if (loading of selectedTab is false) and (title of selectedTab contains lessonID & ".md") then exit repeat
            delay 0.25
        end repeat
        if URL of selectedTab is not lessonURL then error "The tutorial tab did not reach the requested URL."
        if (loading of selectedTab) or (title of selectedTab does not contain lessonID & ".md") then error "The tab opened, but the lesson page title is not verified yet."
        return "reused=" & reused & linefeed & "tab_id=" & id of selectedTab & linefeed & "language=" & lessonLanguage & linefeed & "url=" & URL of selectedTab & linefeed & "title=" & title of selectedTab
    end tell
end run
