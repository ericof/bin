tell application "Address Book"
    set emailList to {}
    set peopleCount to (count every person)
    repeat with i from 1 to peopleCount
        set phoneCount to (count every phone of person i)
        if phoneCount > 0 then
            repeat with p from 1 to phoneCount
                try
                    set phoneValue to my strip_spaces(get value of phone p of person i)
                on error
                    set phoneValue to "xxxx"
                end try
                
                if phoneValue starts with "55-011" then
                    set phoneLen to length of phoneValue
                    set phoneValue to "+5511" & ((characters 7 thru phoneLen of phoneValue) as string)
                end if
                if phoneValue starts with "119" then
                    set phoneLen to length of phoneValue
                    set phoneValue to "+5511" & ((characters 3 thru phoneLen of phoneValue) as string)
                end if
                if phoneValue starts with "117" then
                    set phoneLen to length of phoneValue
                    set phoneValue to "+5511" & ((characters 3 thru phoneLen of phoneValue) as string)
                end if
                if phoneValue starts with "118" then
                    set phoneLen to length of phoneValue
                    set phoneValue to "+5511" & ((characters 3 thru phoneLen of phoneValue) as string)
                end if
                if phoneValue starts with "47" then
                    set phoneLen to length of phoneValue
                    set phoneValue to "+5547" & ((characters 4 thru phoneLen of phoneValue) as string)
                end if                
                if phoneValue starts with "11-" then
                    set phoneLen to length of phoneValue
                    set phoneValue to "+5511" & ((characters 4 thru phoneLen of phoneValue) as string)
                end if
                if phoneValue starts with "(04111)" then
                    set phoneLen to length of phoneValue
                    set phoneValue to "+5511" & ((characters 8 thru phoneLen of phoneValue) as string)
                end if
                if phoneValue starts with "011" then
                    set phoneLen to length of phoneValue
                    set phoneValue to "+5511" & ((characters 4 thru phoneLen of phoneValue) as string)
                end if
                if phoneValue starts with "(11)" then
                    set phoneLen to length of phoneValue
                    set phoneValue to "+5511" & ((characters 5 thru phoneLen of phoneValue) as string)
                end if
                if phoneValue starts with "411" then
                    set phoneLen to length of phoneValue
                    set phoneValue to "+55" & ((characters 3 thru phoneLen of phoneValue) as string)
                end if
                if phoneValue starts with "041" then
                    set phoneLen to length of phoneValue
                    set phoneValue to "+55" & ((characters 4 thru phoneLen of phoneValue) as string)
                end if
                if phoneValue starts with "0" then
                    set phoneLen to length of phoneValue
                    set phoneValue to "+55" & ((characters 2 thru phoneLen of phoneValue) as string)
                end if
                if phoneValue starts with "55 " then
                    set phoneLen to length of phoneValue
                    set phoneValue to "+55" & ((characters 3 thru phoneLen of phoneValue) as string)
                end if
                if (length of phoneValue > 4)
                    set value of phone p of person i to phoneValue
                end if
            end repeat
        end if
    end repeat
end tell

on strip_spaces(aLine)
    --strip  lead spaces
    set ods to AppleScript's text item delimiters
    repeat until first character of aLine is not " "
        
        set AppleScript's text item delimiters to {""}
        set aLine to (characters 2 thru -1 of aLine as string)
        set AppleScript's text item delimiters to ods
    end repeat
    
    --strip tail spaces
    set ods to AppleScript's text item delimiters
    repeat until last character of aLine is not " "
        log aLine
        set AppleScript's text item delimiters to {""}
        set aLine to (characters 1 thru -2 of aLine as string)
        set AppleScript's text item delimiters to ods
    end repeat
    set aLine to my replace(aLine, " - ", "-")
    set aLine to my replace(aLine, ".", "-")
    set aLine to my replace(aLine, "-", "")
    set aLine to my replace(aLine, " ", "")
    set aLine to my replace(aLine, "(", "")
    set aLine to my replace(aLine, ")", "")
    return aLine
end strip_spaces


on replace(sourcetext, search, replacement)
    set oldDelim to AppleScript's text item delimiters
    set AppleScript's text item delimiters to the search
    set the textItemList to every text item of the sourcetext
    set AppleScript's text item delimiters to the replacement
    set the output to the textItemList as string
    set AppleScript's text item delimiters to oldDelim
    return output
end replace