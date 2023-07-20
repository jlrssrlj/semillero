PGDMP     +                    {            postgres    15.3    15.3      %           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            &           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            '           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            (           1262    5    postgres    DATABASE     ~   CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Colombia.1252';
    DROP DATABASE postgres;
                postgres    false            )           0    0    DATABASE postgres    COMMENT     N   COMMENT ON DATABASE postgres IS 'default administrative connection database';
                   postgres    false    3368                        3079    16384 	   adminpack 	   EXTENSION     A   CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;
    DROP EXTENSION adminpack;
                   false            *           0    0    EXTENSION adminpack    COMMENT     M   COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';
                        false    2            �            1259    16409    Cliente    TABLE     �   CREATE TABLE public."Cliente" (
    "Idcliente" integer NOT NULL,
    "Nombre" "char" NOT NULL,
    "Telefono" "char",
    "Direccion" "char"
);
    DROP TABLE public."Cliente";
       public         heap    postgres    false            �            1259    16414    Empleado    TABLE     �   CREATE TABLE public."Empleado" (
    "Idempleado" integer NOT NULL,
    "Nombre" "char" NOT NULL,
    "Fechaingreso" date NOT NULL,
    "Fecharetiro" date,
    cargo "char" NOT NULL,
    "Correo" "char"
);
    DROP TABLE public."Empleado";
       public         heap    postgres    false            �            1259    16419    Producto    TABLE     �   CREATE TABLE public."Producto" (
    "Idproducto" integer NOT NULL,
    "Nombreproducto" "char" NOT NULL,
    "Precio" money NOT NULL,
    codigo integer,
    "Idproveedores" integer NOT NULL
);
    DROP TABLE public."Producto";
       public         heap    postgres    false            �            1259    16452    Proveedores    TABLE     �   CREATE TABLE public."Proveedores" (
    "Idproveedores" integer NOT NULL,
    "Nombre" "char" NOT NULL,
    "Nit" integer NOT NULL,
    "Direccion" "char",
    telefono integer
);
 !   DROP TABLE public."Proveedores";
       public         heap    postgres    false            �            1259    16442    Stock    TABLE     �   CREATE TABLE public."Stock" (
    "Idstock" integer NOT NULL,
    "Disponibles" integer NOT NULL,
    "Stock" integer NOT NULL,
    "Idproducto" integer NOT NULL
);
    DROP TABLE public."Stock";
       public         heap    postgres    false            �            1259    16424    Venta    TABLE       CREATE TABLE public."Venta" (
    "Idventa" integer NOT NULL,
    "HoraInicio" timestamp with time zone NOT NULL,
    "HoraFinal" timestamp with time zone NOT NULL,
    "Idempleado" integer NOT NULL,
    "Idcliente" integer NOT NULL,
    "Idproducto" integer NOT NULL
);
    DROP TABLE public."Venta";
       public         heap    postgres    false            �            1259    16404    login    TABLE        CREATE TABLE public.login (
    "Idempleado" integer NOT NULL,
    "Correo" "char" NOT NULL,
    "Password" "char" NOT NULL
);
    DROP TABLE public.login;
       public         heap    postgres    false                      0    16409    Cliente 
   TABLE DATA           S   COPY public."Cliente" ("Idcliente", "Nombre", "Telefono", "Direccion") FROM stdin;
    public          postgres    false    216   C$                 0    16414    Empleado 
   TABLE DATA           l   COPY public."Empleado" ("Idempleado", "Nombre", "Fechaingreso", "Fecharetiro", cargo, "Correo") FROM stdin;
    public          postgres    false    217   `$                 0    16419    Producto 
   TABLE DATA           g   COPY public."Producto" ("Idproducto", "Nombreproducto", "Precio", codigo, "Idproveedores") FROM stdin;
    public          postgres    false    218   }$       "          0    16452    Proveedores 
   TABLE DATA           `   COPY public."Proveedores" ("Idproveedores", "Nombre", "Nit", "Direccion", telefono) FROM stdin;
    public          postgres    false    221   �$       !          0    16442    Stock 
   TABLE DATA           R   COPY public."Stock" ("Idstock", "Disponibles", "Stock", "Idproducto") FROM stdin;
    public          postgres    false    220   �$                  0    16424    Venta 
   TABLE DATA           p   COPY public."Venta" ("Idventa", "HoraInicio", "HoraFinal", "Idempleado", "Idcliente", "Idproducto") FROM stdin;
    public          postgres    false    219   �$                 0    16404    login 
   TABLE DATA           C   COPY public.login ("Idempleado", "Correo", "Password") FROM stdin;
    public          postgres    false    215   �$       �           2606    16413    Cliente Cliente_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public."Cliente"
    ADD CONSTRAINT "Cliente_pkey" PRIMARY KEY ("Idcliente");
 B   ALTER TABLE ONLY public."Cliente" DROP CONSTRAINT "Cliente_pkey";
       public            postgres    false    216            �           2606    16418    Empleado Empleado_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public."Empleado"
    ADD CONSTRAINT "Empleado_pkey" PRIMARY KEY ("Idempleado");
 D   ALTER TABLE ONLY public."Empleado" DROP CONSTRAINT "Empleado_pkey";
       public            postgres    false    217            �           2606    16423    Producto Producto_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public."Producto"
    ADD CONSTRAINT "Producto_pkey" PRIMARY KEY ("Idproducto");
 D   ALTER TABLE ONLY public."Producto" DROP CONSTRAINT "Producto_pkey";
       public            postgres    false    218            �           2606    16456    Proveedores Proveedores_pkey 
   CONSTRAINT     k   ALTER TABLE ONLY public."Proveedores"
    ADD CONSTRAINT "Proveedores_pkey" PRIMARY KEY ("Idproveedores");
 J   ALTER TABLE ONLY public."Proveedores" DROP CONSTRAINT "Proveedores_pkey";
       public            postgres    false    221            �           2606    16446    Stock Stock_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public."Stock"
    ADD CONSTRAINT "Stock_pkey" PRIMARY KEY ("Idstock");
 >   ALTER TABLE ONLY public."Stock" DROP CONSTRAINT "Stock_pkey";
       public            postgres    false    220            ~           2606    16408    login login_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.login
    ADD CONSTRAINT login_pkey PRIMARY KEY ("Idempleado");
 :   ALTER TABLE ONLY public.login DROP CONSTRAINT login_pkey;
       public            postgres    false    215            �           2606    16432    Venta Cliente    FK CONSTRAINT     �   ALTER TABLE ONLY public."Venta"
    ADD CONSTRAINT "Cliente" FOREIGN KEY ("Idcliente") REFERENCES public."Cliente"("Idcliente") NOT VALID;
 ;   ALTER TABLE ONLY public."Venta" DROP CONSTRAINT "Cliente";
       public          postgres    false    3200    216    219            �           2606    16427    Venta Empleado    FK CONSTRAINT     �   ALTER TABLE ONLY public."Venta"
    ADD CONSTRAINT "Empleado" FOREIGN KEY ("Idempleado") REFERENCES public."Empleado"("Idempleado");
 <   ALTER TABLE ONLY public."Venta" DROP CONSTRAINT "Empleado";
       public          postgres    false    217    3202    219            �           2606    16437    Venta Producto    FK CONSTRAINT     �   ALTER TABLE ONLY public."Venta"
    ADD CONSTRAINT "Producto" FOREIGN KEY ("Idproducto") REFERENCES public."Producto"("Idproducto") NOT VALID;
 <   ALTER TABLE ONLY public."Venta" DROP CONSTRAINT "Producto";
       public          postgres    false    3204    218    219            �           2606    16447    Stock Producto    FK CONSTRAINT     �   ALTER TABLE ONLY public."Stock"
    ADD CONSTRAINT "Producto" FOREIGN KEY ("Idproducto") REFERENCES public."Producto"("Idproducto") NOT VALID;
 <   ALTER TABLE ONLY public."Stock" DROP CONSTRAINT "Producto";
       public          postgres    false    3204    220    218            �           2606    16457    Proveedores Producto    FK CONSTRAINT     �   ALTER TABLE ONLY public."Proveedores"
    ADD CONSTRAINT "Producto" FOREIGN KEY ("Idproveedores") REFERENCES public."Proveedores"("Idproveedores") NOT VALID;
 B   ALTER TABLE ONLY public."Proveedores" DROP CONSTRAINT "Producto";
       public          postgres    false    221    3208    221                  x������ � �            x������ � �            x������ � �      "      x������ � �      !      x������ � �             x������ � �            x������ � �     