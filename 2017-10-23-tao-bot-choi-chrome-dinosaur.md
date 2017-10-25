


# Tao bot version dau tien

with mss() as screenshotter:
    a = find_game_position(screenshotter, threshold = 0.7)
Traceback (most recent call last):

  File "<ipython-input-17-9dbf65ddb8ed>", line 2, in <module>
    a = find_game_position(screenshotter, threshold = 0.7)

  File "<ipython-input-16-561931e4fefa>", line 7, in find_game_position
    for monitor in screenshotter.enum_display_monitors()[1:-1]:

AttributeError: 'MSS' object has no attribute 'enum_display_monitors'


    time.sleep(0.1)
12.5495294673
273.749930495
267.309806163
269.991133119
302.211898942
299.143959505
275.028849203
285.478089872
292.979122557
315.913417452
302.155052345
318.971837692
335.783354321
325.252224467
322.012232609

check_speed_change(speed_array)
Out[209]: 13.120586453473253

    time.sleep(0.01)
1.14820127827
280.697380807
279.455446698
290.222050827
273.689795493
272.647787123
262.197616867
277.654022092
302.041244915
290.195386832
313.64403512
317.861801536
325.764028328

check_speed_change(speed_array)
Out[207]: 11.571918165872619

    time.sleep(0)

13.445771174
249.885998521
273.122355677
288.800433642
292.787836563
295.288920373
296.889103007
278.365999549
287.994216432
293.339599281
293.16754633

check_speed_change(speed_array)

Out[205]: 8.9635400696821907