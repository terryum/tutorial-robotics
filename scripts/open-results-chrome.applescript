-- Keep the book and the experimental results in separate windows.
on run argv
    set pageURL to item 1 of argv
    set pageTitle to item 2 of argv
    set priorID to item 3 of argv
    set priorURL to item 4 of argv
    tell application "Google Chrome"
        set resultWindow to missing value
        set oldWindow to missing value
        repeat with w in windows
            if (id of w as text) is priorID and (count of tabs of w) is 1 then
                if URL of active tab of w is priorURL then
                    if priorURL is pageURL then
                        set resultWindow to w
                    else
                        set oldWindow to w
                    end if
                end if
            end if
        end repeat
        if resultWindow is missing value then
            set resultWindow to make new window
            set URL of active tab of resultWindow to pageURL
        end if
        set index of resultWindow to 1
        activate
        set resultTab to active tab of resultWindow
        repeat 40 times
            if (loading of resultTab is false) and (title of resultTab is pageTitle) then exit repeat
            delay 0.25
        end repeat
        if (URL of resultTab is not pageURL) or (title of resultTab is not pageTitle) or (loading of resultTab) then error "The results page did not load."
        if oldWindow is not missing value then
            if (count of tabs of oldWindow) is 1 and URL of active tab of oldWindow is priorURL then close oldWindow
        end if
        return id of resultWindow as text
    end tell
end run
