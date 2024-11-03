import time
import machine
import utils
import hackaday
import openai
# import display
# import characters

def main():
    print("hello world")

    # my_string = ""

    # while True:
    #     # display.write_text("asdf")
    #     input = characters.poll()
    #     display.write_text(my_string + input)
    #     if btn_a.value() == False:
    #         my_string += input
    #     time.sleep_ms(1)
    # return
    
    # input("press enter to continue")
    utils.connect_to_wifi()


    while True:
        while True:
            led.toggle()
            time.sleep_ms(100)
            if btn_a.value() == False:
                break

        try:
            for article in hackaday.get_articles():
                utils.write_to_typewriter(
                    article
                )

            # response = openai.chatgpt("write an essay about photolithography")
            # utils.write_to_typewriter(response)
            break
        except OSError:
            print("failed to make request")
            pass
    
    while True:
        led.toggle()
        time.sleep(1)

if __name__ == "__main__":
    main()
