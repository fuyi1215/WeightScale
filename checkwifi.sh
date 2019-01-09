ping -c5 10.0.201.104 > /dev/null

if [ $? != 0 ]
then
  sudo /sbin/shutdown -r now
fi
