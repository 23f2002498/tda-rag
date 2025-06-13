# Doubt in GA1 Q4 & Q5

**User**: carlton
**URL**: [https://discourse.onlinedegree.iitm.ac.in/t/doubt-in-ga1-q4-q5/149231/6](https://discourse.onlinedegree.iitm.ac.in/t/doubt-in-ga1-q4-q5/149231/6)

Windows files system is case insensitive. Linux typically uses a case sensitive filesystem (although you can configure it to whatever you wanted).

Typically a VM is completely isolated, however because WSL still has to be accessible to the windows filesystem (you can for example view the WSL filesystem directly from windows file explorer), it seems to have been configured with a case insensitive filesystem. This is odd in your case because Windows documentation seems to suggest the default is otherwise. [Case Sensitivity | Microsoft Learn](https://learn.microsoft.com/en-us/windows/wsl/case-sensitivity)

Google Colab notebooks has a linux backend and currently runs on Ubuntu 22.04  
You can run these in your google colab to see what it runs

> !cat /etc/\*release

This is the file system info

> !df -Th

Incredibly on ext4 (which typically what most default linux systems use), you are even able to enable case insensitivity on a directory by directory basis! (for those power users that have very specific use cases). Windows also claims to now support this feature on NT through the use of directory flags.

Nice bit of work.

Kind regards
