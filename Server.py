import asyncio
import pickle
import socket

def get_ipv4_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error as e:
        return f"Unable to get IP Address: {e}"

try:
    with open("users.pkl", "rb") as file:
        users = pickle.load(file)
except FileNotFoundError:
    users = {}
    with open("users.pkl", "wb") as file:
        pickle.dump(users, file)

async def handle_client(reader, writer):
    try:
        _id = pickle.loads(await reader.read(4096)) 
        print(f"Received: {_id}")
        if _id == 0:
            login_or_signup = pickle.loads(await reader.read(4096))
            print(f"Received: {login_or_signup}")
            if login_or_signup[0] == "Login":
                try:
                    with open("users.pkl", "rb") as file:
                        users = pickle.load(file)
                except FileNotFoundError:
                    users = {}
                if login_or_signup[1] in users and users[login_or_signup[1]] == login_or_signup[2]:
                    print("Success")
                    writer.write(pickle.dumps("Success"))
                    await writer.drain()
                    print("Success")
                else:
                    writer.write(pickle.dumps("Wrong Email or Password"))
                    await writer.drain()
                    print("Wrong Email or Password")

            elif login_or_signup[0] == "Sign_Up":
                try:
                    with open("users.pkl", "rb") as file:
                        users = pickle.load(file)
                except FileNotFoundError:
                    users = {}
                
                if login_or_signup[1] in users:
                    writer.write(pickle.dumps("Yes"))
                    await writer.drain()
                    print("Yes")
                else:
                    writer.write(pickle.dumps("No"))
                    await writer.drain()
                    print("No")

                    user_data = pickle.loads(await reader.read(4096))
                    users[user_data[0]] = user_data[1]

                    with open("users.pkl", "wb") as file:
                        pickle.dump(users, file)

                    writer.write(pickle.dumps("Account added"))
                    await writer.drain()
                    print("Account added")
            
            elif login_or_signup[0] == "Forget Password":
                try:
                    with open("users.pkl", "rb") as file:
                        users = pickle.load(file)
                except FileNotFoundError:
                    users = {}
                
                if login_or_signup[1] in users:
                    writer.write(pickle.dumps("Yes"))
                    await writer.drain()
                    print("Yes")
                    user_data = pickle.loads(await reader.read(4096))
                    users[user_data[0]] = user_data[1]

                    with open("users.pkl", "wb") as file:
                        pickle.dump(users, file)

                    writer.write(pickle.dumps("Account added"))
                    await writer.drain()
                    print("Account added")
                
                else:
                    writer.write(pickle.dumps("No"))
                    await writer.drain()
                    print("No")


            writer.close()
            await writer.wait_closed()

        elif _id == 1:
            client_data_pickled =await reader.read(4096)
            if not client_data_pickled:
                print("Dissconnected")
                return
            client_data = pickle.loads(client_data_pickled)
            print(f"Received: {client_data}")
            print(f"Connected to {client_data}")
            writer.write(pickle.dumps("Connected"))
            await writer.drain()
            print("Connected")

            try:
                with open(f"{client_data}.pkl", "rb") as file:
                    data = pickle.load(file)
                    writer.write(pickle.dumps(data))
                    await writer.drain()
                    print("Data sent")
            except FileNotFoundError:
                data = {"Personal_Chat": [],
                        "Group_Chat": []}
                

                with open(f"{client_data}.pkl", "wb") as file:
                    pickle.dump(data, file)

                writer.write(pickle.dumps(data))
                await writer.drain()
                print("Data sent")
            print(pickle.loads(await reader.read(4096)))
            try:
                with open(f"{client_data}_contacts.pkl", "rb") as file:
                    contacts = pickle.load(file)
                writer.write(pickle.dumps(contacts))
                await writer.drain()
                print("Contacts sent")
            except FileNotFoundError:
                contacts = {}
                with open(f"{client_data}_contacts.pkl", "wb") as file:
                    pickle.dump(contacts, file)
                writer.write(pickle.dumps(contacts))
                await writer.drain()
                print("Contacts sent new")
            while True:
                try:
                    with open(f"{client_data}.pkl", "rb") as file:
                        data = pickle.load(file)

                    with open("users.pkl", "rb") as file:
                        users = pickle.load(file)

                    message = await reader.read(4096)
                    try:
                        if pickle.loads(message)[0] == "Exit":
                            print("Closing intiated")
                            contacts = pickle.loads(message)[1]
                            with open(f"{client_data}_contacts.pkl", "wb") as file:
                                pickle.dump(contacts, file)
                            print("Client disconnected")
                            break
                    except:
                        pass
                            

                    message_data = pickle.loads(message)
                    if len(message_data["Personal_Chat"]) > len(data["Personal_Chat"]):
                        print(f"1. Data: {data}, Message_data: {message_data}")
                        data = message_data
                        print(f"2. Data: {data}, Message_data: {message_data}")
                        with open(f"{client_data}.pkl", "wb") as file:
                            pickle.dump(data, file)
                        recivers_email = data["Personal_Chat"][-1]["Reciever_email"]
                        print(f"3. Reciever email: {recivers_email}")
                        print(f"4. MY email: {client_data}, Reciever email: {recivers_email}, Boolean: {client_data != recivers_email}")
                        if client_data != recivers_email:
                            print("5. Not the same")
                            if recivers_email in users.keys():
                                with open(f"{recivers_email}.pkl", "rb") as file:
                                    reciver_data = pickle.load(file)
                                reciver_data["Personal_Chat"].append(message_data["Personal_Chat"][-1])
                                print(f"6. Reciver data: {reciver_data}")
                                with open(f"{recivers_email}.pkl", "wb") as file:
                                    pickle.dump(reciver_data, file)

                    writer.write(pickle.dumps(data))
                    await writer.drain()

                except Exception as e:
                    print(f"Error from sending or recieving: {e}")
                    return

        elif _id == 2:
            try:
                message = await reader.read(4096)
                with open("users.pkl", "rb") as file:
                    users = pickle.load(file)
                print(f"Received: {pickle.loads(message)}")
                if pickle.loads(message)[0] == "Add Contact":
                    contact_email = pickle.loads(message)[1]
                    print(f"Adding contact {contact_email}")
                    if contact_email in users.keys():
                        writer.write(pickle.dumps("Yes"))
                        await writer.drain()
                    else:
                        writer.write(pickle.dumps("No"))
                        await writer.drain()
                        print("No")
                        
            except Exception as e:
                print(f"Error from adding contact: {e}")

    except Exception as e:
        print(f"Error reading the data: {e}")
        return
    finally:
        print(f"Closing connection")
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, get_ipv4_address(), 8888)
    print("Server is running. Waiting for clients...")

    async with server:
        await server.serve_forever()

asyncio.run(main())