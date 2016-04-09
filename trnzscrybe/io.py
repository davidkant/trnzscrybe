def export_staff(staff, staffname, filename):

  f = open(filename, 'w')
  f.write('\"' + staffname + '\" = {\n')
  f.write(staff.__format__()[12:-1]) # this cuts off the \new staff part...
  f.write('\n}')
  f.close()
