#include <string.h>
int is_palindrome(char* text)
{
    int i, len;
    len = strlen(text);
    for (i = 0; i< len / 2; i++)
        if (text[i] != text[len - i - 1])
            return 0;
    return 1;
}
